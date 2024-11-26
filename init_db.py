import mysql.connector
from mysql.connector import Error

def execute_sql_file(file_path, host, user, password, database):
    try:
        # Connessione al database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print(f"Connessione al database {database} avvenuta con successo!")

            # Legge il contenuto del file SQL
            with open(file_path, 'r') as file:
                sql_commands = file.read()

            # Esegui le istruzioni SQL
            cursor = connection.cursor()
            for command in sql_commands.split(';'):
                if command.strip():  # Se la query non è vuota
                    cursor.execute(command)
                    print(f"Comando eseguito con successo: {command[:60]}...")  # Mostra una parte del comando eseguito

            # Commit delle modifiche
            connection.commit()
            print("Inizializzazione completata con successo!")

    except Error as e:
        print(f"Errore durante l'esecuzione dello script SQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connessione al database chiusa.")

# Parametri di connessione (modifica con i tuoi dati)
db_host = "localhost"  # Modifica con l'indirizzo del tuo server DB
db_user = "your_user"  # Modifica con il tuo nome utente DB
db_password = "your_password"  # Modifica con la tua password DB
db_name = "munchkin"  # Modifica con il nome del tuo database

# Percorso del file SQL da eseguire
file_path = "init_db.sql"  # Modifica con il percorso del file .sql

# Esegui lo script
execute_sql_file(file_path, db_host, db_user, db_password, db_name)
