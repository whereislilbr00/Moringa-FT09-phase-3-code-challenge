from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.save_db()

    def __repr__(self):
        return f'<Author {self.name}>'
    
    def save_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self.name,))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

# Id     
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id    

# Name
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")
        
        
# articles  
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, title FROM articles WHERE author_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()

        return articles
    
    @staticmethod
    def get_by_id(author_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT *FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            author = Author(row[1])
            author.id = row[0]
            return author
        return None
