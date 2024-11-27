import os


database_config = {
    "host": os.environ.get("DB_HOST", "placeholder"),
    "port": os.environ.get("DB_PORTS", 3306),
    "user": os.environ.get("DB_USER", "placeholder"),
    "password": os.environ.get("DB_PASSWORD", "placeholder"),
    "database": os.environ.get("DB_NAME", "placeholder"),
}

flask_app_config = {
    "debug": os.environ.get("FLUSK_DEBUG_OPTION", True),
    "host": os.environ.get("FLASK_HOST", "0.0.0.0"),
    "port": os.environ.get("FLASK_PORT", 5000),
}


class Config:
    # Configurazione generica per l'app Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")

    # Configurazione del database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # La stringa di connessione al database MySQL
    # Modifica con il tuo username, password e IP del database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql://{}:{}@{}/{}".format(
            database_config["user"],
            database_config["password"],
            database_config["host"],
            database_config["database"],
        ),
    )
