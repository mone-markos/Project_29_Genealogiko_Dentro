def display_family_tree():
    
    canvas.delete("all")  # Διαγραφή περιεχομένου(εαν υπάρχει)
    canvas.create_text(350, 50, text="Γενεαλογικό Δέντρο", font=("Arial", 16, "bold"))

    # Ανάκτηση των δεδομένων από τη βάση
    cursor.execute("SELECT * FROM person")
    persons = cursor.fetchall()

    # Σχεδιασμός ατόμων
    positions = {}  # Αποθηκεύουμε τις θέσεις για κάθε άτομο
    y_position = 400

    # άτομα (παππούδες, γονείς, παιδιά)
    for person in persons:
        id, name, last_name, relationship, parent_id = person
        
        # Δημιουργία του κουτιού για το άτομο
        rect = canvas.create_rectangle(300, y_position, 500, y_position + 50, fill="lightpink")
        canvas.create_text(400, y_position + 25, text=f"{name} {last_name} ({relationship})", font=("Arial", 12))

        # Προσθήκη event για το κλικ πάνω στο κουτάκι
        canvas.tag_bind(rect, "<Button-1>", lambda event, id=id, name=name, last_name=last_name, relationship=relationship: show_person_details(id, name, last_name, relationship))

        # Αποθήκευση της θέσης του ατόμου
        positions[id] = (350, y_position + 25)

        # Ανάλογα με την θέση του πατέρα ή της μητέρας γίνεται η επόμενη τοποθέτηση
        if relationship == "Grandfather" or relationship == "Grandmother":
            y_position -= 150
        elif relationship == "Father" or relationship == "Mother":
            y_position -= 100
        else:  #παιδιά
            y_position -= 50

    # Γραμμές σχέσεων
    for person in persons:
        id, name, last_name, relationship, parent_id = person
        if parent_id is not None:
            parent_position = positions.get(parent_id)
            if parent_position:
                if relationship == "Child":
                    line_color = "pink"  # Γραμμή για γονέα-παιδί (ροζ)
                elif relationship == "Partner":
                    line_color = "red"  # Γραμμή για ζευγάρι (κόκκινη)
                else:
                    line_color = "black"  # Αν δεν είναι γονέας ή ζευγάρι, μαύρη γραμμή
                
                # Σύνδεση με τον γονιό ή τον σύντροφο
                canvas.create_line(parent_position[0], parent_position[1], positions[id][0], positions[id][1], width=2, fill=line_color)
