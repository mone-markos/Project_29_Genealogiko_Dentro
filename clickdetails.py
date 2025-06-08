def show_details(id, name, last_name, relationship):
    # pop-up
    details_window = Toplevel(root)
    details_window.title(f"Στοιχεία {name} {last_name}")
    details_window.geometry("300x200")
    details_window.config(bg="#9fc5e8")

    # Προσθήκη των στοιχείων του ατόμου στο νέο παράθυρο
    Label(details_window, text=f"Όνομα: {name} {last_name}", font=("Arial", 12), bg="#9fc5e8").pack(pady=10)
    Label(details_window, text=f"Σχέση: {relationship}", font=("Arial", 12), bg="#9fc5e8").pack(pady=10)
    
    # Kουμπί για κλείσιμο του pop-up
    Button(details_window, text="Κλείσιμο", command=details_window.destroy, font=("Arial", 10)).pack(pady=10)
