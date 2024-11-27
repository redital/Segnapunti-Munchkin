from flask import Flask, render_template, request, redirect, url_for
from config import Config, flask_app_config
from database import db
from models import Player, Game, CurrentGamePlayer, Victory
from datetime import date


app = Flask(__name__)
app.config.from_object(Config)  # Carica la configurazione dal file config.py
db.init_app(app)  # Inizializza il database con l'app Flask

@app.route('/')
def index():
    # Recupera tutti i giocatori (per le checkbox)
    players = Player.query.all()

    # Recupera l'ID della partita corrente
    current_game = Game.query.order_by(Game.id.desc()).first()  # Ottieni l'ultimo gioco inserito
    if current_game and current_game.is_active:
        # Recupera i giocatori che sono associati a questa partita
        current_game_players = CurrentGamePlayer.query.filter_by(game_id=current_game.id).all()
    else:
        current_game_players = []

    # Ottieni i giocatori che sono nella partita corrente con i loro livelli
    current_players = []
    for gp in current_game_players:
        player = Player.query.get(gp.player_id)
        if player:
            current_players.append({
                'player': player,
                'level': gp.level  # Aggiungi il livello dal modello CurrentGamePlayer
            })

    # Passa sia tutti i giocatori (per le checkbox) sia i giocatori partecipanti alla partita (con i livelli) alla vista
    return render_template('index.html', players=players, current_game_players=current_game_players, current_players=current_players)



@app.route('/add_player', methods=['POST'])
def add_player():
    name = request.form['name']
    if name:
        # Controllo se il giocatore esiste già nel database
        player = Player.query.filter_by(name=name).first()
        if not player:
            player = Player(name=name)
            db.session.add(player)
            db.session.commit()
    return redirect(url_for('index'))

@app.route('/remove_player/<int:id>')
def remove_player(id):
    # Rimuove un giocatore dalla partita ma non dal database
    player = CurrentGamePlayer.query.filter_by(player_id=id).first()
    if player:
        db.session.delete(player)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_level/<int:player_id>/<string:level_change>', methods=['GET'])
def update_level(player_id, level_change):
    # Recupera l'ID dell'ultima partita creata (partita corrente)
    current_game = Game.query.order_by(Game.id.desc()).first()

    if current_game:
        # Recupera il giocatore specifico nella partita corrente
        current_game_player = CurrentGamePlayer.query.filter_by(player_id=player_id, game_id=current_game.id).first()

        if current_game_player:
            # Determina la modifica del livello
            if level_change == "p1":
                current_game_player.level += 1  # Incrementa il livello
            elif level_change == "m1":
                if current_game_player.level > 1:  # Evita che il livello scenda sotto 1
                    current_game_player.level -= 1  # Decrementa il livello
            else:
                return redirect(url_for('index'))  # Se il level_change non è valido, ritorna all'indice

            # Controlla se il giocatore ha raggiunto il livello 10
            if current_game_player.level >= 10:
                # Segna il giocatore come vincitore
                current_game_player.is_winner = True
                db.session.commit()

            # Salva le modifiche nel database
            db.session.commit()

    # Torna alla pagina principale
    return redirect(url_for('index'))


@app.route('/start_game', methods=['POST'])
def start_game():
    # Controlla se ci sono partite attive
    active_game = Game.query.filter_by(is_active=True).first()
    if active_game:
        active_game.is_active = False  # Disattiva la partita precedente
        db.session.commit()

    # Crea una nuova partita
    game = Game()  # La nuova partita ha un'ora di inizio
    db.session.add(game)
    db.session.commit()

    # Aggiungi i giocatori alla partita
    for player_id in request.form.getlist('players'):
        player = Player.query.get(player_id)
        if player:
            current_game_player = CurrentGamePlayer(player_id=player.id, game_id=game.id)
            db.session.add(current_game_player)

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/end_game', methods=['POST'])
def end_game():
    # Recupera l'ID della partita corrente
    current_game = Game.query.filter_by(is_active=True).first()

    if current_game:
        # Imposta la partita come inattiva
        current_game.is_active = False
        db.session.commit()

        # Rimuove i giocatori dalla tabella current_game_players
        current_game_players = CurrentGamePlayer.query.filter_by(game_id=current_game.id).all()

        # Per ogni giocatore, aggiorniamo il contatore delle partite giocate e la vittoria, se applicabile
        for current_game_player in current_game_players:
            player = Player.query.get(current_game_player.player_id)

            if player:
                # Incrementiamo il numero totale di partite giocate
                player.total_games += 1

                # Se il giocatore è un vincitore, incrementiamo il numero di vittorie
                if current_game_player.is_winner:
                    player.total_wins += 1

                    # Salviamo una nuova vittoria nel database
                    new_victory = Victory(player_id=player.id, win_date=date.today())
                    db.session.add(new_victory)

        # Salviamo le modifiche
        db.session.commit()

        db.session.commit()

    # Torna alla pagina principale
    return redirect(url_for('index'))


@app.route('/record_win/<int:player_id>')
def record_win(player_id):
    player = Player.query.get_or_404(player_id)
    player.total_wins += 1
    
    # Incrementa le partite giocate per tutti i giocatori nella partita corrente
    current_game_players = CurrentGamePlayer.query.filter_by(player_id=player_id).all()
    for current_game_player in current_game_players:
        current_player = Player.query.get(current_game_player.player_id)
        if current_player:
            current_player.total_games += 1
    
    db.session.commit()

    # Registra la vittoria
    new_victory = Victory(player_id=player_id, win_date=date.today())
    db.session.add(new_victory)
    db.session.commit()

    return redirect(url_for('ranking'))

@app.route('/ranking')
def ranking():
    top_players = db.session.query(Player, db.func.count(Victory.id).label('win_count'), Player.total_games) \
        .join(Victory) \
        .group_by(Player.id) \
        .order_by(db.desc('win_count')) \
        .all()

    # Aggiungi la percentuale di vittorie
    players_with_percentages = []
    for player, win_count, total_games in top_players:
        if total_games > 0:
            win_percentage = (win_count / total_games) * 100
        else:
            win_percentage = 0
        players_with_percentages.append((player, win_percentage, win_count, total_games))
    
    return render_template('ranking.html', players=players_with_percentages)

if __name__ == '__main__':
    app.run(**flask_app_config)

