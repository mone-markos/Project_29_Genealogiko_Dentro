from tkinter import *
from tkinter.font import Font
import Database
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox

def display_family_tree():
    """Αναπαριστά και εμφανίζει το γενεαλογικό δέντρο με τα δεδομένα από τη βάση δεδομένων."""
    G = nx.Graph()  # Δημιουργία γράφου

    # Λήψη όλων των ατόμων από τη βάση δεδομένων
    people = Database.get_all_people()
    for person in people:
        # Προσθέτουμε κόμβο με όνομα, επώνυμο και ημερομηνία γέννησης
        G.add_node(person[0], 
                   name=f"{person[1]} {person[2]}",  # Full name
                   first_name=person[1],
                   last_name=person[2],
                   birth_date=person[3],
                   id=person[0])  # Προσθέτουμε το id του ατόμου

    # Λήψη όλων των σχέσεων από τη βάση δεδομένων
    relationships = Database.get_all_relationships()
    for relationship in relationships:
        person1_id, person2_id, relation_type = relationship[1], relationship[2], relationship[3]

        if relation_type == 'parent' or relation_type == 'child':
            color = 'purple'
        elif relation_type == 'spouse':
            color = 'red'
        elif relation_type == 'sibling':
            color = 'pink'

        G.add_edge(person1_id, person2_id, relation_type=relation_type, color=color)

    # Απεικόνιση του γενεαλογικού δέντρου με matplotlib
    pos = nx.spring_layout(G)  # Θέση των κόμβων

    edges = G.edges(data=True)
    colors = [data['color'] for u, v, data in edges]

    # Δημιουργία figure και axis για matplotlib
    fig, ax = plt.subplots(figsize=(12, 10))

    # Προσαρμογή μεγέθους κειμένου ώστε να χωράει μέσα στους κόμβους
    node_labels = nx.get_node_attributes(G, 'name')
    
    # Χρησιμοποιούμε nx.draw με labels
    nx.draw(G, pos, with_labels=True, labels=node_labels,
            node_size=3000, node_color="lightblue", font_size=9, 
            edge_color=colors, ax=ax, font_family="Arial", font_color="black")

    # Δημιουργία του canvas για να ενσωματώσουμε το matplotlib figure στο Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)  # Εδώ το canvas το ενσωματώνουμε στο root παράθυρο
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    # Κλικ σε κόμβο για εμφάνιση πληροφοριών
    def on_click(event):
        """Χειρίζεται το κλικ στους κόμβους και εμφανίζει τις πληροφορίες μέσω παραθύρου διαλόγου."""
        # Υπολογισμός της απόστασης του κλικ από τους κόμβους και εμφάνιση των πληροφοριών
        for node in G.nodes:
            # Υπολογισμός της απόστασης του κλικ από τους κόμβους
            node_pos = pos[node]
            distance = ((event.x - node_pos[0] * 500) ** 2 + (event.y - node_pos[1] * 500) ** 2) ** 0.5
            if distance < 20:  # Αν η απόσταση είναι μικρή από τον κόμβο (20 pixels)
                person = Database.get_person(node)
                info_text = f"ID: {person[0]}\nName: {person[1]} {person[2]}\nBorn: {person[3]}"
                
                # Εμφάνιση των πληροφοριών σε παράθυρο διαλόγου
                messagebox.showinfo("Person Info", info_text)

    # Συνδέουμε το click event με το παράθυρο Tkinter
    root.bind("<Button-1>", on_click)
