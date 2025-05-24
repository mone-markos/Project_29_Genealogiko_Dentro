# CRUD
# C: Create
# R: Read (h find h whatever)
# U: Update
# D: Delete
import sqlite3
from datetime import date
from person import Person

class Database:
    def __init__(self):
        # dhmioyrgia twn table, an den yparxoyn
        self.conn = sqlite3.connect("family_tree.db")
        print(f"Successfully connected to database")

        # people table
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
            UNIQUE(person_id_1, person_id_2, relationship_type) -- Avoid duplicate relationships
        );
        """)
    
    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()


    # C (Person)
    # epistrefei ?
    def insert_person(self, name, last_name, date_of_birth):
        # otan thes na trekseis mia entolh SQL:

        # 1. thn ftiaxneis san string
        sql = ''' INSERT INTO people(name, last_name, date_of_birth)
              VALUES(?,?,?) '''
        
        # 2. ftiaxneis ena "cursor"
        cursor = self.conn.cursor()

        # 3. ekteleis thn entolh (vazeis mesa parametroys)
        cursor.execute(sql, (name, last_name, date_of_birth))

        # 4. oristikopoiei thn allagh (save sthn vash)
        self.conn.commit()

        return cursor.lastrowid

    # C (Relationship)
    def insert_relationship(self, id1, id2, relationship_type):
        sql = ''' INSERT INTO relationships(person_id_1, person_id_2, relationship_type)
              VALUES(?,?,?) '''
        cursor = self.conn.cursor()

        cursor.execute(sql, (id1, id2, relationship_type))
        self.conn.commit()


    # R (Person, Relationship)
    def get_all_people(self):
        sql = "SELECT * FROM people;"
        cursor = self.conn.cursor()

        cursor.execute(sql)
        
        people = []
        people_sql = cursor.fetchall()

        for person_sql in people_sql:
            people.append(Person(id=person_sql[0], name=person_sql[1], last_name=person_sql[2], date_of_birth=date.fromisoformat(person_sql[3])))
        

        sql = "SELECT * FROM relationships;"
        cursor.execute(sql)
        relationships_sql = cursor.fetchall()
        print('relationships:', relationships_sql)

        # ftiaxnw prwta syzhgoys
        for relationship in relationships_sql:
            id1 = relationship[1]
            id2 = relationship[2]
            relationship_type = relationship[3]

            # stoxos: prepei to person me id1 na exei spouse to person me id2 sthn lista
            # kai antistrofa
            
            for person in people:
                if person.id == id1:
                    person1 = person
                    break 

            for person in people:
                if person.id == id2:
                    person2 = person
                    break 

            if relationship_type == 'spouse':
                person1.spouse = person2 
                person2.spouse = person1
            else:
                person1.children.append(person2)
                person2.parents.append(person1)

        return people
    
    # U (Person)
    def update_person(self, id, name=None, last_name=None, date_of_birth=None):
        sql = "UPDATE people SET name = ?, last_name = ?, date_of_birth = ? WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (name, last_name, date_of_birth, id))
        self.conn.commit()
    
    # D (Person)
    def delete_person(self, id):
        sql = "DELETE FROM people WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, [id])
        self.conn.commit()

    # D (Relationship)
    def delete_relationship(self, id1, id2):
        sql = "DELETE FROM relationships WHERE person_id_1 = ? AND person_id_2 = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (id1,id2))
        self.conn.commit()
    
    def delete_all_relationship_of_person_id(self, id):
        sql = "DELETE FROM relationships WHERE person_id_1 = ? OR person_id_2 = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (id, id))
        self.conn.commit()
    