import sqlite3


def registration(dbname, username, password, status='user'):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f'''INSERT INTO Users (username, password, status)
VALUES ('{username}', '{password}', '{status}')''')
    connection.commit()
    connection.close()


def finduserstatus(dbname, username):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f'''SELECT status FROM Users WHERE username = '{username}' ''')
    result = cursor.fetchall()
    connection.close()
    return result[0][0]


def addlevel(dbname, levelname, leveltext, leveltype, creator='void'):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f'''INSERT INTO Levels (levelname, leveltext,leve;type, creator)
VALUES ('{levelname}', '{leveltext}', '{leveltype}', '{creator}')''')
    connection.commit()
    connection.close()


def findlevel(dbname, levelname):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM Levels WHERE levelname = '{levelname}' ''')
    result = cursor.fetchall()
    connection.close()
    return result


def addentity(dbname, entname, enttext, enttype, usedlevels, creator='void'):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f'''INSERT INTO Entities (entname, enttext, enttype, usedlevels, creator)
VALUES ('{entname}', '{enttext}', '{enttype}', '{usedlevels}', '{creator}')''')
    connection.commit()
    connection.close()


def findentity(dbname, entname):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * FROM Entities WHERE entname = '{entname}' ''')
    result = cursor.fetchall()
    connection.close()
    return result


def authorization(dbname, username, password):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(f'''SELECT status FROM Users WHERE username = '{username}'
AND passsword = '{password}' ''')
    result = cursor.fetchall()
    connection.close()
    return result[0][0]
