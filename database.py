import sqlite3 as db
import config

def createTables():
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(config.USER_TABLE_SQL)
        cur.execute(config.DATA_TABLE_SQL)
    return True


def getTotalRows(table):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        quarry = f"SELECT Count(*) FROM {table}"
        cur.execute(quarry)
        return cur.fetchall()[0][0]

# UserPart

def insertUser(username,password,power_level):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(f"""
        INSERT INTO {config.USER_TABLE_NAME} (username,password,power) VALUES ("{username}","{password}",{power_level})
        """)
        con.commit()
        return True

def checkUserExists(username):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM {config.USER_TABLE_NAME} WHERE username = '{username}' LIMIT 1""")
        if cur.fetchone():
            return True
        else:
            return False

def checkUserExistsByID(user_id):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT username FROM {config.USER_TABLE_NAME} WHERE id = '{user_id}' LIMIT 1""")
        if cur.fetchone():
            return True
        else:
            return False

def checkUserCorrect(username,password):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM {config.USER_TABLE_NAME} WHERE username = '{username}' AND password = '{password}' LIMIT 1""")
        if cur.fetchone():
            return True
        else:
            return False

def getUserPower(username):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT power FROM {config.USER_TABLE_NAME} WHERE username = '{username}' LIMIT 1""")
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return False

def getUsers():
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM {config.USER_TABLE_NAME}""")
        return cur.fetchall()

def deleteUser(user_id):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(f"""
        DELETE FROM {config.USER_TABLE_NAME} WHERE id = '{user_id}'
        """)
        con.commit()
        return True

# DataPart

def insertData(file_name,date,count,price,user1_precedent,user2_precedent,user3_precedent,user4_precedent,user5_precedent,desc):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(f"""
        INSERT INTO {config.DATA_TABLE_NAME}
        (file_name,date,count,price,user1_precedent,user2_precedent,user3_precedent,user4_precedent,user5_precedent,desc) 
        VALUES ("{file_name}","{date}",{count},{price},{user1_precedent},{user2_precedent},{user3_precedent},{user4_precedent},{user5_precedent},"{desc}")
        """)
        con.commit()
        return True

def changeData(file_id,file_name,date,count,price,user1_precedent,user2_precedent,user3_precedent,user4_precedent,user5_precedent,desc):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(f"""
            UPDATE {config.DATA_TABLE_NAME} SET
            file_name = '{file_name}',
            date = '{date}',
            count = '{count}',
            price = '{price}',
            user1_precedent = '{user1_precedent}',
            user2_precedent = '{user2_precedent}',
            user3_precedent  = '{user3_precedent}',
            user4_precedent  = '{user4_precedent}',
            user5_precedent  = '{user5_precedent}',
            desc = '{desc}'
            WHERE id = {file_id}
        """)
        con.commit()
        return True

def deleteData(file_id):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(f"""
        DELETE FROM {config.DATA_TABLE_NAME} WHERE id = '{file_id}'
        """)
        con.commit()
        return True

def getDatas(reverse=False,statement1=1,statement2=1):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        quarry = f"""
            SELECT * 
            FROM {config.DATA_TABLE_NAME}
            ORDER BY id DESC
        """
        cur.execute(quarry)
        
        raw_data = cur.fetchall()

        i = 0
        data = []
        for row in raw_data:
            if i >= statement1 and i <= statement2:
                data.append(row)
            i += 1
        
        return data

def getDataByID(id):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        quarry = f"SELECT * FROM {config.DATA_TABLE_NAME} WHERE id = '{id}'"
        cur.execute(quarry)
        return cur.fetchone()

def checkDataExists(file_id):
    with db.connect(config.DB_NAME) as con:
        cur = con.cursor()
        quarry = f"SELECT * FROM {config.DATA_TABLE_NAME} WHERE id = '{file_id}'"
        cur.execute(quarry)
        if cur.fetchone():
            return True
        else:
            return False