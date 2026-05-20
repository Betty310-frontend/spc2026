import sqlite3

class MyDatabase():
    def __init__(self):
        self.db = sqlite3.connect('board.sqlite3', check_same_thread=False)
        self.cursor = self.db.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS board (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(50) NOT NULL,
            message VARCHAR(200) NOT NULL
        )
        """)
    
    def execute(self, query, args=()):
        self.cursor.execute(query, args)

    def execute_fetch(self, query, args=()):
        self.cursor.execute(query, args)
        result = self.cursor.fetchall()
        return result
    
    def commit(self):
        self.db.commit()

if __name__ == '__main__':
    db = MyDatabase()
    db.execute("INSERT INTO board (title, message) VALUES (?, ?)", ("첫 번째 게시글", "안녕하세요!"))
    db.commit()