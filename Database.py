import sqlite3
from datetime import date
from person import Person

class Database:
    def __init__(self):
        # Συνδέεται ή δημιουργεί το αρχείο της βάσης δεδομένων
        self.conn = sqlite3.connect("family_tree.db")
        print("Successfully connected to database")

        # Δημιουργεί τον πίνακα people αν δεν υπάρχει ήδη
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth DATE
        );
        """)

        # Δημιουργεί τον πίνακα relationships αν δεν υπάρχει ήδη
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

    # ------------------ Δημιουργία ------------------

    def insert_person(self, name, last_name, date_of_birth):
        # Προσθέτει ένα νέο άτομο στη βάση
        sql = '''INSERT INTO people(name, last_name, date_of_birth) VALUES(?,?,?)'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (name, last_name, date_of_birth))
        self.conn.commit()
        return cursor.lastrowid

    def insert_relationship(self, id1, id2, relationship_type):
        # Προσθέτει μια νέα σχέση μεταξύ δύο ατόμων
        sql = '''INSERT INTO relationships(person_id_1, person_id_2, relationship_type) VALUES(?,?,?)'''
        cursor = self.conn.cursor()
        cursor.execute(sql, (id1, id2, relationship_type))
        self.conn.commit()

    # ------------------ Ανάγνωση ------------------

    def get_person(self, person_id):
        # Επιστρέφει ένα αντικείμενο Person με βάση το ID
        sql = "SELECT * FROM people WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (person_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return Person(id=row[0], name=row[1], last_name=row[2], date_of_birth=date.fromisoformat(row[3]))
        return None

    def get_all_people(self):
        # Επιστρέφει λίστα όλων των ατόμων με τις σχέσεις τους
        sql = "SELECT * FROM people"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        people = []
        for row in cursor.fetchall():
            people.append(Person(id=row[0], name=row[1], last_name=row[2], date_of_birth=date.fromisoformat(row[3])))

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

    # ------------------ Ενημέρωση ------------------

    def update_person(self, person_id, name=None, last_name=None, date_of_birth=None):
        # Ενημερώνει τα στοιχεία ενός ατόμου
        sql = "UPDATE people SET name = ?, last_name = ?, date_of_birth = ? WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (name, last_name, date_of_birth, person_id))
        self.conn.commit()

    def update_relationship_by_id(self, relationship_id, new_type):
        # Ενημερώνει μια σχέση με βάση το ID της σχέσης
        sql = "UPDATE relationships SET relationship_type = ? WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (new_type, relationship_id))
        self.conn.commit()

    # ------------------ Διαγραφή ------------------

    def delete_person(self, person_id):
        # Διαγράφει ένα άτομο με βάση το ID
        sql = "DELETE FROM people WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (person_id,))
        self.conn.commit()

    def delete_relationship(self, id1, id2):
        # Διαγράφει μια σχέση μεταξύ δύο ατόμων
        sql = "DELETE FROM relationships WHERE person_id_1 = ? AND person_id_2 = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (id1, id2))
        self.conn.commit()

    def delete_relationship_by_id(self, relationship_id):
        # Διαγράφει μια σχέση με βάση το ID της
        sql = "DELETE FROM relationships WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (relationship_id,))
        self.conn.commit()

    def delete_all_relationships_of_person(self, person_id):
        # Διαγράφει όλες τις σχέσεις ενός συγκεκριμένου ατόμου
        sql = "DELETE FROM relationships WHERE person_id_1 = ? OR person_id_2 = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (person_id, person_id))
        self.conn.commit()

    # ------------------ Εργαλεία Ανάπτυξης ------------------

    def show_people(self):
        # Εμφανίζει όλα τα άτομα στη βάση (για έλεγχο)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM people")
        print("\nΆτομα στη βάση:")
        for row in cursor.fetchall():
            print(row)
        cursor.close()

    def show_relationships(self):
        # Εμφανίζει όλες τις σχέσεις (για έλεγχο)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM relationships")
        print("\nΣχέσεις στη βάση:")
        for row in cursor.fetchall():
            print(row)
        cursor.close()

# ------------------ Singleton Αντικείμενο για απλοποιημένη χρήση ------------------

_db = Database()

# ------------------ Wrapper Συναρτήσεις για χρήση από το GUI ------------------

def add_person(name, last_name, date_of_birth):
    return _db.insert_person(name, last_name, date_of_birth)

def get_person(person_id):
    person = _db.get_person(int(person_id))
    if person:
        return [person.id, person.name, person.last_name, person.date_of_birth.isoformat() or ""]
    return None

def delete_person(person_id):
    return _db.delete_person(int(person_id))

def add_relationship(id1, id2, rel_type):
    return _db.insert_relationship(int(id1), int(id2), rel_type)

def get_relationship(relationship_id):
    cursor = _db.conn.cursor()
    sql = "SELECT * FROM relationships WHERE id = ?"
    cursor.execute(sql, (int(relationship_id),))
    row = cursor.fetchone()
    cursor.close()
    return row

def update_relationship_by_id(relationship_id, new_type):
    return _db.update_relationship_by_id(int(relationship_id), new_type)

def delete_relationship_by_id(relationship_id):
    return _db.delete_relationship_by_id(int(relationship_id))