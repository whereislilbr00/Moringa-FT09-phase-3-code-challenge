from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
        self.save_db()

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    def save_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self.name, self.category))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()
# id
    @property
    def id (self):
        return self._id
    
    @id.setter
    def id (self, id):
        self._id = id
# Name
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if type(name) is str and 2 <= len(name) <= 16: 
             self._name = name
        else:
            raise ValueError("Name must be between 2 and 16 characters")
# Category    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        if  isinstance(category, str) and len(category) > 0:
             self._category = category
        else:
            raise ValueError("Category must be a non-empty string")
        
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, title FROM articles WHERE magazine_id = ?",(self.id,))
        articles = cursor.fetchall()
        conn.close()

        return articles
    
    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(''' SELECT DISTINCT authors.id, authors.name FROM authors
                            JOIN articles ON authors.id = articles.author_id
                            WHERE articles.magazine_id = ?
                       ''',(self.id,))
        
        contributors = cursor.fetchall()
        conn.close()

        return contributors
    
    @staticmethod
    def get_id(magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM magazines WHERE id =?", (magazine_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            magazine = Magazine(row[1], row[2])
            magazine.id = row[0]
            return magazine
        return None

