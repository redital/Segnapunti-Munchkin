-- Crea il database 'munchkin' (se non esiste già)
CREATE DATABASE IF NOT EXISTS munchkin;

-- Seleziona il database appena creato
USE munchkin;

-- Crea la tabella per i giocatori (players)
CREATE TABLE IF NOT EXISTS players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    total_wins INT DEFAULT 0,
    total_games INT DEFAULT 0,
    UNIQUE(name)
);

-- Crea la tabella per le partite (games)
CREATE TABLE IF NOT EXISTS games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Crea la tabella di relazione per i giocatori attivi nelle partite (current_game_players)
CREATE TABLE IF NOT EXISTS current_game_players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    player_id INT NOT NULL,
    level INT DEFAULT 1,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
);

-- Crea la tabella per salvare le vittorie (victories)
CREATE TABLE IF NOT EXISTS victories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    win_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
);

-- Crea l'indice per ottimizzare la ricerca delle vittorie per giocatore
CREATE INDEX idx_player_id ON victories(player_id);

-- (Opzionale) Aggiungi qualche dato di test per i giocatori predefiniti
INSERT INTO players (name) 
VALUES 
    ('Raffaello'),
    ('Francesco'),
    ('Ettore'),
    ('Pierclaudio');

