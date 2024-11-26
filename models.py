from datetime import datetime
from database import db

# Modello per la tabella players
class Player(db.Model):
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    total_wins = db.Column(db.Integer, default=0)
    total_games = db.Column(db.Integer, default=0)

    # Relazione con le partite
    current_games = db.relationship('CurrentGamePlayer', backref='player', lazy=True)

    # Relazione con le vittorie
    victories = db.relationship('Victory', backref='player', lazy=True)

# Modello per la tabella games
class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relazione con i giocatori
    players = db.relationship('Player', secondary='current_game_players', backref='games')

# Modello per la tabella current_game_players (giocatori della partita corrente)
class CurrentGamePlayer(db.Model):
    __tablename__ = 'current_game_players'
    
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    level = db.Column(db.Integer, default=1)

# Modello per la tabella victories (storico vittorie)
class Victory(db.Model):
    __tablename__ = 'victories'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    win_date = db.Column(db.Date, default=datetime.utcnow)
    
    # Relazione con il giocatore
    player = db.relationship('Player', backref=db.backref('victories', lazy=True))
