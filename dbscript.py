import sqlite3

def createDatabase(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS user(username TEXT PRIMARY KEY,password TEXT, firstname TEXT, lastname TEXT, email TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS city(cityID INTEGER PRIMARY KEY AUTOINCREMENT, cityname TEXT)")

    c.execute("""CREATE TABLE IF NOT EXISTS event(eventid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,description TEXT, price FLOAT, date DATE, time TIME, isActive BOOLEAN,
     location TEXT,cityID INTEGER, username TEXT, FOREIGN KEY (cityID) REFERENCES city(cityID), FOREIGN KEY (username) REFERENCES user(username))""")

def insertRecord(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT OR IGNORE INTO user VALUES(?,?,?,?,?)", ("test1", "123", "testname", "testsurname", "test@test.com"))
    c.execute("INSERT OR IGNORE INTO user VALUES(?,?,?,?,?)", ("test2", "123","test2name", "test2surname", "test2@test.com"))

    c.execute("INSERT OR IGNORE INTO event(name,description,price,date,time,location,cityID) VALUES(?,?,?,?,?,?,?)",("TestEv", "TestDec", "TestP", "1-1-1111", "11:11","TestLoc","2"))

    c.execute("INSERT INTO city(cityname) VALUES('Lefkosa')")
    c.execute("INSERT INTO city(cityname) VALUES('Girne')")
    c.execute("INSERT INTO city(cityname) VALUES('Guzelyurt')")
    c.execute("INSERT INTO city(cityname) VALUES('Gazi Magusa')")
    c.execute("INSERT INTO city(cityname) VALUES('Lefke')")
    c.execute("INSERT INTO city(cityname) VALUES('Iskele')")

    conn.commit()

if __name__ == "__main__":
    createDatabase("eventwebsite.db")
    insertRecord("eventwebsite.db")