from tkinter import *
from tkinter.font import Font
from Database import *
import networkx as nx
import matplotlib.pyplot as plt
import tkinter.messagebox

# Συνάρτηση σύνδεσης με τη βάση δεδομένων
def connect_db():
    return sqlite3.connect('family_tree.db')

# Δημιουργία του γράφου
G = nx.Graph()

# Φόρτωση των ατόμων και των σχέσεων από τη βάση δεδομένων
def load_persons_and_relationships():
    conn = connect_db()
    cursor = conn.cursor()

    # Λήψη των ατόμων
    cursor.execute('SELECT * FROM people')
    people = cursor.fetchall()

    # Προσθήκη των ατόμων ως κόμβοι στον γράφο
    for person in people:
        person_id, first_name, last_name, birth_date, description = person
        # Δημιουργία label
        G.add_node(person_id, label=f'{first_name} {last_name} ({person_id})', info=description)

    # Λήψη όλων των σχέσεων από τη βάση δεδομένων
    cursor.execute('SELECT * FROM relationships')
    relationships = cursor.fetchall()
    # Προσθήκη των σχέσεων στον γράφο
    for relationship in relationships:
        person1_id, person2_id, relation_type = relationship[1], relationship[2], relationship[3]

        if relation_type == 'parent' or relation_type == 'child':
            color = 'purple'
        elif relation_type == 'spouse':
            color = 'red'
        elif relation_type == 'sibling':
            color = 'pink'

        # Προσθήκη της σχέσης ως γραμμή στον γράφο
        G.add_edge(person1_id, person2_id, color=color, relation=relation_type)

    conn.close()

def show_popup(node_id):
    """Αναπαράγει το pop-up για το άτομο που επιλέγεται από το γράφημα."""
    person = get_person(node_id)  # Ανάκτηση των πληροφοριών από τη βάση δεδομένων
    if person:
        first_name, last_name, birth_date, description = person[1], person[2], person[3], person[4]
        message = f"Όνομα: {first_name} {last_name}\nΗμερομηνία Γέννησης: {birth_date}\nΠεριγραφή: {description}"
        tkinter.messagebox.showinfo("Πληροφορίες Ατόμου", message)

def display_family_tree():
    """Εμφανίζει το γενεαλογικό δέντρο με matplotlib."""
    load_persons_and_relationships()  # Φορτώνουμε τα δεδομένα πριν από την εμφάνιση του γράφου

    pos = nx.spring_layout(G)  # εμφάνιση κυκλακίων
    node_labels = nx.get_node_attributes(G, 'label')  # Ετικέτες για τους κόμβους
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]  # Χρώμα γραμμών

    # Δημιουργία γραφήματος με matplotlib
    fig, ax = plt.subplots(figsize=(10, 10))

    # Σχεδιάζουμε το γράφημα
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color='lightgrey', edge_color=edge_colors,
            node_size=3000, font_size=12, font_weight='bold', width=2, ax=ax)

    # Ρύθμιση γραμματοσειράς
    for label in node_labels.values():
        if len(label) > 20:  # Αν το όνομα είναι πολύ μεγάλο, μειώνουμε το μέγεθος της γραμματοσειράς
            font_size = 8
        else:
            font_size = 12
        nx.draw_networkx_labels(G, pos, font_size=font_size, font_weight='bold')

    # Συνάρτηση για να ανιχνεύουμε το κλικ στον κόμβο
    def on_click(event, ax, G):
        """Ελέγχει αν έγινε κλικ σε κάποιον κόμβο και εμφανίζει τα στοιχεία του σε pop-up."""
        for node in G.nodes():
            x, y = pos[node]  # Θέση του κόμβου
            distance = ((event.xdata - x) ** 2 + (event.ydata - y) ** 2) ** 0.5  # Απόσταση του κλικ
            if distance < 0.1:  # Αν το κλικ είναι κοντά στον κόμβο
                show_popup(node)  # Εμφανίζουμε το pop-up

    # Εγγραφή του κλικ στον άξονα
    fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, ax, G))

    # Τίτλος και εμφάνιση του γραφήματος
    plt.title("Γενεαλογικό Δέντρο", fontsize=15)
    plt.show()
