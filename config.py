import os

class Config:
    # Configurazione generica per l'app Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')
    
    # Configurazione del database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # La stringa di connessione al database MySQL
    # Modifica con il tuo username, password e IP del database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://username:password@ip-del-db/munchkin')
