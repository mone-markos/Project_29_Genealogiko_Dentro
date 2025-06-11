from Database import *
import networkx as nx
import matplotlib.pyplot as plt
import tkinter.messagebox

# Σύνδεση με τη βάση δεδομένων και το αρχείο που δημιουργείται
def connect_db():
    return sqlite3.connect('family_tree.db')

# Αποθήκευση μεταβλητής G
G = nx.Graph()

# Φόρτωση των ατόμων και των σχέσεων τους από τη database
def load_persons_and_relationships():
    conn = connect_db()
    cursor = conn.cursor()

    # Λήψη όλων των ατόμων από database
    cursor.execute('SELECT * FROM people')
    people = cursor.fetchall()

    # Επεξεργασία ατόμων από πίνακα people και ορισμός μεταβλητών
    for person in people:
        person_id = person[0]
        first_name = person[1]
        last_name = person[2]
        birth_date = person[3]

        # Δημιουργία label για τον κόμβο με το ID και το όνοματεπώνυμο 
        G.add_node(person_id, label=f'(ID:{person_id})\n{first_name}\n{last_name}')

    # Λήψη όλων των σχέσεων από database
    cursor.execute('SELECT * FROM relationships')
    relationships = cursor.fetchall()
    
    # Προσθήκη των σχέσεων στον γράφο με χρωματική κωδικοποίηση
    for relationship in relationships:
        person1_id, person2_id, relation_type = relationship[1], relationship[2], relationship[3]

        if relation_type == 'parent' or relation_type == 'child':
            color = 'purple'
        elif relation_type == 'spouse':
            color = 'red'
        elif relation_type == 'sibling':
            color = 'blue'

        # Ορισμός σχέσης ως γραμμή
        G.add_edge(person1_id, person2_id, color=color, relation=relation_type)

    #κλείσιμο σύνδεσης
    conn.close()

# Ορισμός pop up με παράμετρο
def show_popup(node_id):   
    person = get_person(node_id) #Συλλέγει τις πληροφορίες από τη database
    if person: 
        person[1], person[2], person[3]
        message = f"Όνομα: {person[1]} {person[2]}\nΗμερομηνία Γέννησης: {person[3]}"
        tkinter.messagebox.showinfo("Πληροφορίες Ατόμου", message)
        
# Εμφάνιση δέντρου
def display_family_tree():
    
    load_persons_and_relationships()  # Φορτώνουμε τα δεδομένα

    pos = nx.spring_layout(G, k=0.5)  # Ορισμός pos για την θέση των κόμβων, k για να μην κάνουν overlap
    node_labels = nx.get_node_attributes(G, 'label')  # Ετικέτες για τους κόμβους
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]  # Χρωματισμός γραμμών

    # Δημιουργία γραφήματος
    fig, ax = plt.subplots(figsize=(8, 8))

    # Σχεδιάσμος γραφήματος
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color='lightgrey', edge_color=edge_colors,
            node_size=7000, font_size=10, font_weight='light', width=2, ax=ax)

    # Συνάρτηση για το κλικ στον κόμβο
    def on_click(event, ax, G):      
        for node in G.nodes():
            x, y = pos[node]  # Θέση του κόμβου στον άξoνα
            distance = ((event.xdata - x) ** 2 + (event.ydata - y) ** 2) ** 0.5  # Απόσταση του κλικ
            if distance < 0.1:
                show_popup(node)  # Εμφανίζουμε το pop-up
                
    #Αποτύπωση του κλικ στον άξονα
    fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, ax, G))

    # Τίτλος και εμφάνιση του γραφήματος   
    plt.title("Χρωματική κωδικοποίηση:\n Μωβ = Γονείς-Παιδί Κόκκινο = Ζευγάρι Μπλε = Αδέρφια", fontsize=12)
    plt.show()
