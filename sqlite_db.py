import sqlite3, datetime

db = 'userpool.db'  # Data base name


def start_user_database():
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
      username VARCHAR(50) PRIMARY KEY UNIQUE NOT NULL,
      password TEXT NOT NULL )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS log (
      username VARCHAR(50) NOT NULL,
      action VARCHAR(100) NOT NULL,
      time DATATIME NOT NULL,
      FOREIGN KEY(username) REFERENCES users(username))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS visit_counter (
      username VARCHAR(50) PRIMARY KEY UNIQUE NOT NULL,
      number_visits INTEGER DEFAULT 1,
      FOREIGN KEY(username) REFERENCES users(username))''')

    cursor = connection.execute("SELECT username FROM users WHERE username=?", ['Anonymous'])
    if not cursor.fetchone():  # Anonymous already exists, no need to create this user
        connection.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           ('Anonymous', '6666'));  # Anonymous password won't ever be used (but can't be null)

    connection.commit()
    connection.close()


def login_authentication(username: str, password: str) -> bool:
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor = connection.execute("SELECT username, password FROM users WHERE username=? AND password=?", (username, password))
    if cursor.fetchone():  # Correct username and password, login successful
        connection.execute("UPDATE visit_counter SET number_visits=number_visits+1 WHERE username=?", [username]);
        connection.execute("INSERT INTO log (username, action, time) VALUES (?, ?, ?)", (username, "Login successful", datetime.datetime.now()));
        connection.commit()
        login = True
    else:  # Wrong username and/or passsword, login failed
        login = False
    connection.close()
    return login


def register_new_user(username: str, password: str) -> bool:
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor = connection.execute("SELECT username, password FROM users WHERE username=?", [username])
    if cursor.fetchone():  # Username already exists, can't register
        registration = False
    else:
        connection.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password));
        connection.execute("INSERT INTO visit_counter (username) VALUES (?)", [username]);
        connection.execute("INSERT INTO log (username, action, time) VALUES (?, ?, ?)", (username, "Registration successful", datetime.datetime.now()));
        connection.commit()
        registration = True
    connection.close()
    return registration


def new_entry_log(username: str, action: str):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    connection.execute("INSERT INTO log (username, action, time) VALUES (?, ?, ?)", (username, action, datetime.datetime.now()));
    connection.commit()
    connection.close()


def login_anonymous():
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor = connection.execute("SELECT username FROM visit_counter WHERE username=?", ['Anonymous'])
    if cursor.fetchone():  # Anonymous visit counter exists, need to update it (+1)
        connection.execute("UPDATE visit_counter SET number_visits=number_visits+1 WHERE username=?", ['Anonymous'])
    else:  # Anonymous visit counter does not exist, need to create it
        connection.execute("INSERT INTO visit_counter (username) VALUES (?)", ['Anonymous'])

    connection.execute("INSERT INTO log (username, action, time) VALUES (?, ?, ?)", ('Anonymous', "Login successful", datetime.datetime.now()))
    connection.commit()
    connection.close()


def delete_user_database():  # Only delete IF they already exist => avoid errors
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor = connection.execute("SELECT name FROM userpool.db WHERE type='table' AND username=users")
    if cursor.fetchone():
        cursor.execute("DROP TABLE users")
    cursor = connection.execute("SELECT name FROM userpool.db WHERE type='table' AND username=log")
    if cursor.fetchone():
        cursor.execute("DROP TABLE log")
    cursor = connection.execute("SELECT name FROM userpool.db WHERE type='table' AND name=visit_counter")
    if cursor.fetchone():
        cursor.execute("DROP TABLE visit_counter")

    connection.commit()
    connection.close()

# cursor = connection.execute("SELECT name, password FROM users")
# for row in cursor:
#   print("name = ", row[0])
#   print("password = ", row[1], "\n")
