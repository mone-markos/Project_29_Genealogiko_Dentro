def show_person_details(id, first_name, last_name, birth_date, relation_type):
    # Δημιουργία ενός νέου παραθύρου (pop-up)
    details_window = Toplevel(root)
    details_window.title(f"Στοιχεία: ")
    details_window.geometry("300x200")
    details_window.config(bg="#fdfd96")

    # Προσθήκη των στοιχείων του ατόμου στο νέο παράθυρο
    Label(details_window, text=f"Όνομα: {first_name} {last_name}", font=("Arial", 12), bg="#fdfd96").pack(pady=10)
    Label(details_window, text=f"Ημερομηνία Γέννησης: {birth_date}", font=("Arial", 12), bg="#fdfd96").pack(pady=10)
    Label(details_window, text=f"Σχέση: {relation_type}", font=("Arial", 12), bg="#fdfd96").pack(pady=10)
    
    # Προσθήκη κουμπιού για κλείσιμο του pop-up παραθύρου
    Button(details_window, text="Κλείσιμο", command=details_window.destroy, font=("Arial", 10)).pack(pady=10)
