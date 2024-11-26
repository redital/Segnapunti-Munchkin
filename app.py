from flask import Flask, render_template, request, redirect, url_for
from config import Config
from database import db
from models import Player, Game, CurrentGamePlayer, Victory

app = Flask(__name__)
app.config.from_object(Config)  # Carica la configurazione dal file config.py
db.init_app(app)  # Inizializza il database con l'app Flask

@app.route('/')
def index():
    players = Player.query.all()
    return render_template('index.html', players=players)

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

@app.route('/update_level/<int:id>/<int:level_change>')
def update_level(id, level_change):
    player = CurrentGamePlayer.query.filter_by(player_id=id).first()
    if player:
        player.level += level_change
        if player.level < 1:
            player.level = 1
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/start_game', methods=['POST'])
def start_game():
    # Crea una nuova partita
    game = Game()
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

@app.route('/record_win/<int:player_id>')
def record_win(player_id):
    player = Player.query.get_or_404(player_id)
    player.total_wins += 1
    player.total_games += 1
    db.session.commit()
    
    new_victory = Victory(player_id=player_id)
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
    app.run(debug=True, host='0.0.0.0')
