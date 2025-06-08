def display_family_tree():
    canvas.create_text(350, 50, text="Γενεαλογικό Δέντρο", font=("Arial", 16, "bold"))  # Τίτλος

    # Ανάκτηση των δεδομένων των ατόμων από τη βάση δεδομένων
    cursor.execute("SELECT * FROM people")
    people = cursor.fetchall()
    cursor.execute("SELECT * FROM relationships")
    relationships = cursor.fetchall()

    # Σχεδιασμός των ατόμων
    positions = {}  # Αποθηκεύουμε τις θέσεις για κάθε άτομο
    y_position = 400  # Ξεκινάμε από το κάτω μέρος

    # Σχεδιάζουμε τα άτομα (παππούδες, γονείς, παιδιά)
    for person in people:
        id, first_name, last_name, relation_type, birth_date, parent_id = person
        
        # Δημιουργία του στρογγυλού κόμβου για το άτομο
        rect = canvas.create_oval(250, y_position, 450, y_position + 50, fill="lightblue")
        canvas.create_text(350, y_position + 25, text=f"{first_name} {last_name} ({relation_type})", font=("Arial", 12))

        # Προσθήκη event για το κλικ πάνω στο κουτάκι
        canvas.tag_bind(rect, "<Button-1>", lambda event, id=id, first_name=first_name, last_name=last_name, relation_type=relation_type, birth_date=birth_date: show_person_details(id, first_name, last_name, relation_type, birth_date))

        # Αποθήκευση της θέσης του ατόμου
        positions[id] = (350, y_position + 25)

    # Σύνδεση γραμμών (για σχέσεις)
    for person in people:
        id, first_name, last_name, relation_type, parent_id = person
        if parent_id is not None:
            parent_position = positions.get(parent_id)
            if parent_position:
                # Καθορίζουμε το χρώμα της γραμμής ανάλογα με τη σχέση
                if relationship == "Child":
                    line_color = "pink"  # Γραμμή για γονέα-παιδί (ροζ)
                elif relationship == "Spouse":
                    line_color = "red"  # Γραμμή για ζευγάρι (κόκκινη)
                elif relationship == "Sibling":
                    line_color = "purple"  # Γραμμή για αδέλφια
                else:
                    line_color = None
                
                # Σύνδεση με τον γονιό ή τον σύντροφο
                canvas.create_line(parent_position[0], parent_position[1], positions[id][0], positions[id][1], width=2, fill=line_color)

    # Σχέση Αδέλφια (sibling)
    for person in people:
        id, first_name, last_name, relation_type, parent_id = person
        # Βρίσκουμε τα αδέλφια με το ίδιο parent_id
        if parent_id is not None:
            siblings = [sibling for sibling in people if sibling[4] == parent_id and sibling[0] != id]
            for sibling in siblings:
                sibling_id, sibling_name, sibling_last_name, sibling_relationship, sibling_parent_id = sibling
                sibling_position = positions.get(sibling_id)
                if sibling_position:
                    # Συνδέουμε τα αδέλφια με μια γραμμή
                    canvas.create_line(positions[id][0], positions[id][1], sibling_position[0], sibling_position[1], width=2, fill="purple")
