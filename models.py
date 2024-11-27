from datetime import datetime
from database import db

# Modello per la tabella players
class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    total_wins = db.Column(db.Integer, default=0)
    total_games = db.Column(db.Integer, default=0)

    # Relazione con CurrentGamePlayer
    current_game_players = db.relationship('CurrentGamePlayer', backref='player_reference')  # Cambiato in 'player_reference'

    # Relazione con Victory
    victories = db.relationship('Victory', backref='winner_player')  # Cambiato in 'winner_player'

# Modello per la tabella games
class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)  # Manteniamo il campo start_time
    is_active = db.Column(db.Boolean, default=True)  # Indica se la partita è attiva

    # Relazione verso CurrentGamePlayer
    current_game_players = db.relationship('CurrentGamePlayer', backref='related_game')  # Cambiato in 'related_game'



# Modello per la tabella current_game_players (giocatori della partita corrente)
class CurrentGamePlayer(db.Model):
    __tablename__ = 'current_game_players'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    level = db.Column(db.Integer, default=1)
    is_winner = db.Column(db.Boolean, default=False)  # Aggiungi questa colonna per indicare il vincitore

    # Relazione verso Player
    player = db.relationship('Player', backref='current_participations')  # Cambiato in 'current_participations'


# Modello per la tabella victories (storico vittorie)
class Victory(db.Model):
    __tablename__ = 'victories'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    win_date = db.Column(db.Date, default=datetime.utcnow)

    # Relazione verso il giocatore
    player = db.relationship('Player', backref='all_victories')  # Cambiato in 'all_victories'
