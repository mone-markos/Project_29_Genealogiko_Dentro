import sqlite3

def show_people():
    conn = sqlite3.connect("family_tree.db")  # Σύνδεση στη βάση
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM people")  # Query για όλα τα άτομα
    people = cursor.fetchall()  # Παίρνουμε όλα τα δεδομένα
    
    conn.close()

    for person in people:
        print(person)  # Εκτυπώνουμε κάθε εγγραφή


def show_relationships():
    """Εμφανίζει όλες τις σχέσεις από τη βάση δεδομένων."""
    conn = sqlite3.connect("family_tree.db")  # Σύνδεση στη βάση
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM relationships")  # Query για όλες τις σχέσεις
    relationships = cursor.fetchall()  # Παίρνουμε όλα τα δεδομένα
    
    conn.close()

    print("\nΣχέσεις στη βάση:")
    for relation in relationships:
        print(relation)  # Εκτύπωση σχέσεων



# Κλήση της συνάρτησης για να εμφανίσει τα δεδομένα
show_people()
print('\n.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.')

show_relationships()
