import sqlite3, datetime

db = 'userpool.db'   #Data base name

def start_user_database():
   connection = sqlite3.connect(db)
   cursor = connection.cursor()

   cursor.execute('''CREATE TABLE IF NOT EXISTS users (
      name VARCHAR(50) PRIMARY KEY UNIQUE NOT NULL,
      password TEXT NOT NULL )''')

   cursor.execute('''CREATE TABLE IF NOT EXISTS log (
      name VARCHAR(50) NOT NULL,
      action VARCHAR(100) NOT NULL,
      time DATATIME NOT NULL,
      FOREIGN KEY(name) REFERENCES usuarios(name))''')

   cursor.execute('''CREATE TABLE IF NOT EXISTS visit_counter (
      name VARCHAR(50) PRIMARY KEY UNIQUE NOT NULL,
      number_visits INTEGER DEFAULT 1,
      FOREIGN KEY(name) REFERENCES usuarios(name))''')

   cursor = connection.execute("SELECT name FROM users WHERE name=?", ('Anonymous'))
   if not cursor.getchone():  # Anonymous already exists, no need to create this user
      connection.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, '6666'));   #Anonymous password won't ever be used (but can't be null)

   connection.commit()
   connection.close()

def login_authentication(name:str, password:str) -> bool:
   connection = sqlite3.connect(db)
   cursor = connection.cursor()

   cursor = connection.execute("SELECT name, password FROM users WHERE name=? AND password=?", (name, password))
   if cursor.getchone():   # Correct username and password, login successful
      connection.execute("UPDATE visit_counter SET number_visits=number_visits+1 WHERE name=?", (name));
      connection.execute("INSERT INTO log (name, action, time) VALUES (?, ?, ?)", (name, "Login successful", datetime.datetime.now()));
      connection.commit()
      login = True
   else:                   # Wrong username and/or passsword, login failed
      login = False
   connection.close()
   return login

def register_new_user(name:str, password:str) -> bool:
   connection = sqlite3.connect(db)
   cursor = connection.cursor()

   cursor = connection.execute("SELECT name, password FROM users WHERE name=?", (name))
   if cursor.getchone():  # Username already exists, can't register
      registration = False
   else:
      connection.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password));
      connection.execute("INSERT INTO visit_counter (name) VALUES (?)", (name));
      connection.execute("INSERT INTO log (name, action, time) VALUES (?, ?, ?)", (name, "Registration successful", datetime.datetime.now()));
      connection.commit()
      registration = True
   connection.close()
   return registration

def new_entry_log(name:str, action:str):
   connection = sqlite3.connect(db)
   cursor = connection.cursor()
   connection.execute("INSERT INTO log (name, action, time) VALUES (?, ?, ?)", (name, action, datetime.datetime.now()));
   connection.commit()
   connection.close()

def login_anonymous():
   connection = sqlite3.connect(db)
   cursor = connection.cursor()

   cursor = connection.execute("SELECT name FROM visit_counter WHERE name=?", ('Anonymous'))
   if cursor.getchone():   # Anonymous visit counter exists, need to update it (+1)
      connection.execute("UPDATE visit_counter SET number_visits=number_visits+1 WHERE name=?", (name))
   else:                   # Anonymous visit counter doesn't exists, need to create it
      connection.execute("INSERT INTO visit_counter (name) VALUES (?)", ('Anonymous'))

   connection.execute("INSERT INTO log (name, action, password) VALUES (?, ?, ?)", ('Anonymous', "Login successful", datetime.datetime.now()))
   connection.commit()
   connection.close()


def delete_user_database():                              #Only delete IF they already exist => avoid errors
   connection = sqlite3.connect(db)
   cursor = connection.cursor()

   cursor = connection.execute("SELECT name FROM userpool.db WHERE type='table' AND name=users")
   if cursor.getchone():
      cursor.execute("DROP TABLE users")
   cursor = connection.execute("SELECT name FROM userpool.db WHERE type='table' AND name=log")
   if cursor.getchone():
      cursor.execute("DROP TABLE log")
   cursor = connection.execute("SELECT name FROM userpool.db WHERE type='table' AND name=visit_counter")
   if cursor.getchone():
      cursor.execute("DROP TABLE visit_counter")

   connection.commit()
   connection.close()


#cursor = connection.execute("SELECT name, password FROM users")
#for row in cursor:
#   print("name = ", row[0])
#   print("password = ", row[1], "\n")