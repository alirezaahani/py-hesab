ADMIN_POWER_LEVEL = 2
USERS_POWER_LEVEL = 1



# Database part
DB_NAME = "sahm.sqlite"
USER_TABLE_NAME = "Users"
DATA_TABLE_NAME = "Datas"

USER_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {USER_TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    power INTAGER
)
"""

DATA_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {DATA_TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT,
    date TEXT,
    count INTAGER,
    price INTAGER,
    user1_precedent INTAGER,
    user2_precedent INTAGER,
    user3_precedent INTAGER,
    user4_precedent INTAGER,
    user5_precedent INTAGER,
    desc TEXT
)
"""