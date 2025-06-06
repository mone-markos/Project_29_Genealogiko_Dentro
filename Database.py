import sqlite3

# Δημιουργεί σύνδεση με τη βάση δεδομένων SQLite
def connect_db():
    return sqlite3.connect("family_tree.db")

# Δημιουργεί τους πίνακες people και relationships αν δεν υπάρχουν ήδη
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birth_date TEXT,
        description TEXT
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person1_id INTEGER NOT NULL,
        person2_id INTEGER NOT NULL,
        relation_type TEXT CHECK (relation_type IN ('parent', 'spouse', 'sibling', 'child')),
        FOREIGN KEY (person1_id) REFERENCES people(id) ON DELETE CASCADE,
        FOREIGN KEY (person2_id) REFERENCES people(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()

# Προσθέτει νέο άτομο στη βάση και επιστρέφει το ID του
def add_person(first_name, last_name, birth_date, description=""):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO people (first_name, last_name, birth_date, description)
    VALUES (?, ?, ?, ?)""", (first_name, last_name, birth_date, description))
    
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

# Ενημερώνει τα στοιχεία ενός υπάρχοντος ατόμου
def update_person(person_id, first_name, last_name, birth_date, description=""):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE people
    SET first_name = ?, last_name = ?, birth_date = ?, description = ?
    WHERE id = ?
    """, (first_name, last_name, birth_date, description, person_id))
    conn.commit()
    conn.close()

# Επιστρέφει τα στοιχεία ενός ατόμου με βάση το ID
def get_person(person_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people WHERE id = ?", (person_id,))
    person = cursor.fetchone()
    conn.close()
    return person

# Επιστρέφει όλα τα άτομα από τη βάση
def get_all_people():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")
    people = cursor.fetchall()
    conn.close()
    return people

# Διαγράφει άτομο και όλες τις σχετικές σχέσεις του
def delete_person(person_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM relationships WHERE person1_id = ? OR person2_id = ?", (person_id, person_id))
    cursor.execute("DELETE FROM people WHERE id = ?", (person_id,))
    conn.commit()
    conn.close()

# Προσθέτει νέα σχέση μεταξύ δύο ατόμων
def add_relationship(person1_id, person2_id, relation_type):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO relationships (person1_id, person2_id, relation_type)
    VALUES (?, ?, ?)""", (person1_id, person2_id, relation_type))
    conn.commit()
    conn.close()

# Επιστρέφει τα στοιχεία μιας σχέσης με βάση το ID της
def get_relationship(relationship_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relationships WHERE id = ?", (relationship_id,))
    relationship = cursor.fetchone()
    conn.close()
    return relationship

# Ενημερώνει τα στοιχεία μιας υπάρχουσας σχέσης
def update_relationship(relationship_id, person1_id, person2_id, relation_type):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE relationships
    SET person1_id = ?, person2_id = ?, relation_type = ?
    WHERE id = ?
    """, (person1_id, person2_id, relation_type, relationship_id))
    conn.commit()
    conn.close()

# Διαγράφει μια σχέση από τη βάση
def delete_relationship(relationship_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM relationships WHERE id = ?", (relationship_id,))
    conn.commit()
    conn.close()

# Επιστρέφει όλες τις σχέσεις από τη βάση
def get_all_relationships():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM relationships")
    relationships = cursor.fetchall()
    conn.close()
    return relationships

# Δημιουργεί τους πίνακες όταν φορτωθεί το αρχείο
create_tables()