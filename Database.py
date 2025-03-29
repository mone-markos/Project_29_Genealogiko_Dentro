import sqlite3

# Σύνδεση στη βάση δεδομένων
def connect_db():
    return sqlite3.connect("family_tree.db")


# Δημιουργία των πινάκων
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


# Προσθήκη ατόμου
def add_person(first_name, last_name, birth_date, description=""):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO people (first_name, last_name, birth_date, description)
    VALUES (?, ?, ?, ?)""", (first_name, last_name, birth_date, description))

    conn.commit()
    conn.close()


# Προσθήκη σχέσης μεταξύ δύο ατόμων
def add_relationship(person1_id, person2_id, relation_type):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO relationships (person1_id, person2_id, relation_type)
    VALUES (?, ?, ?)""", (person1_id, person2_id, relation_type))

    conn.commit()
    conn.close()


# Εύρεση ατόμου με βάση το ID
def get_person(person_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM people WHERE id = ?", (person_id,))
    person = cursor.fetchone()

    conn.close()
    return person


# Εύρεση απογόνων ενός ατόμου
def get_descendants(person_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p.id, p.first_name, p.last_name, p.birth_date 
    FROM people p
    JOIN relationships r ON p.id = r.person2_id
    WHERE r.person1_id = ? AND r.relation_type = 'parent'
    """, (person_id,))

    descendants = cursor.fetchall()

    conn.close()
    return descendants


# Διαγραφή ατόμου και των σχέσεων του
def delete_person(person_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Διαγραφή των σχέσεων του ατόμου
    cursor.execute("DELETE FROM relationships WHERE person1_id = ? OR person2_id = ?", (person_id, person_id))

    # Διαγραφή του ατόμου
    cursor.execute("DELETE FROM people WHERE id = ?", (person_id,))

    conn.commit()
    conn.close()


# Προβολή ολόκληρου του γενεαλογικού δέντρου
def display_family_tree(person_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p1.id, p1.first_name, p1.last_name, p1.birth_date, r.relation_type, p2.id, p2.first_name, p2.last_name 
    FROM people p1
    JOIN relationships r ON p1.id = r.person1_id
    JOIN people p2 ON r.person2_id = p2.id
    WHERE p1.id = ?
    """, (person_id,))

    family_members = cursor.fetchall()

    conn.close()
    return family_members


# Αρχικοποίηση της βάσης και των πινάκων
create_tables()