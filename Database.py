import sqlite3
from datetime import date
from person import Person

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("family_tree.db")
        print("Successfully connected to database")

        self.execute_query("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth DATE
        );
        """)

        self.execute_query("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id_1 INTEGER NOT NULL,
            person_id_2 INTEGER NOT NULL,
            relationship_type TEXT NOT NULL CHECK(relationship_type IN ('parent', 'spouse')),
            FOREIGN KEY (person_id_1) REFERENCES people (id) ON DELETE CASCADE,
            FOREIGN KEY (person_id_2) REFERENCES people (id) ON DELETE CASCADE,
            UNIQUE(person_id_1, person_id_2, relationship_type)
        );
        """)

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    # ------------------ C ------------------

    def insert_person(self, name, last_name, date_of_birth):
        sql = '''INSERT INTO people(name, last_name, date_of_birth) VALUES(?,?,?)'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (name, last_name, date_of_birth))
        self.conn.commit()
        return cursor.lastrowid

    def insert_relationship(self, id1, id2, relationship_type):
        sql = '''INSERT INTO relationships(person_id_1, person_id_2, relationship_type) VALUES(?,?,?)'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (id1, id2, relationship_type))
        self.conn.commit()

    # ------------------ R ------------------

    def get_person(self, person_id):
        sql = "SELECT * FROM people WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (person_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return Person(id=row[0], name=row[1], last_name=row[2], date_of_birth=date.fromisoformat(row[3]))
        return None

    def get_all_people(self):
        sql = "SELECT * FROM people"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        people = []
        for row in cursor.fetchall():
            people.append(Person(id=row[0], name=row[1], last_name=row[2], date_of_birth=date.fromisoformat(row[3])))

        # Add relationships
        cursor.execute("SELECT * FROM relationships")
        for rel in cursor.fetchall():
            id1, id2, rel_type = rel[1], rel[2], rel[3]
            p1 = next((p for p in people if p.id == id1), None)
            p2 = next((p for p in people if p.id == id2), None)
            if p1 and p2:
                if rel_type == 'spouse':
                    p1.spouse = p2
                    p2.spouse = p1
                else:
                    p1.children.append(p2)
                    p2.parents.append(p1)
        cursor.close()
        return people

    # ------------------ U ------------------

    def update_person(self, person_id, name=None, last_name=None, date_of_birth=None):
        sql = "UPDATE people SET name = ?, last_name = ?, date_of_birth = ? WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (name, last_name, date_of_birth, person_id))
        self.conn.commit()

    def update_relationship(self, id1, id2, new_type):
        sql = "UPDATE relationships SET relationship_type = ? WHERE person_id_1 = ? AND person_id_2 = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (new_type, id1, id2))
        self.conn.commit()

    # ------------------ D ------------------

    def delete_person(self, person_id):
        sql = "DELETE FROM people WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (person_id,))
        self.conn.commit()

        
    def delete_relationship(self, id1, id2):
        sql = "DELETE FROM relationships WHERE person_id_1 = ? AND person_id_2 = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (id1, id2))
        self.conn.commit()

    def delete_all_relationships_of_person(self, person_id):
        sql = "DELETE FROM relationships WHERE person_id_1 = ? OR person_id_2 = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (person_id, person_id))
        self.conn.commit()

    # ------------------ Debug Helpers ------------------

    def show_people(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM people")
        print("\nΆτομα στη βάση:")
        for row in cursor.fetchall():
            print(row)
        cursor.close()

    def show_relationships(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM relationships")
        print("\nΣχέσεις στη βάση:")
        for row in cursor.fetchall():
            print(row)
        cursor.close()
