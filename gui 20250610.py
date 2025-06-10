from tkinter import *
from tkinter.font import Font
from Database import *
import networkx as nx
import matplotlib.pyplot as plt
import tkinter.messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
'''
periexomena:

DHMIOURGIA
def open_add_person_window(): OK
def open_add_relationship_window(): dhmiourgei thn sxesh, den epistrefei id

EPEKSERGASIA
def open_edit_relationship_window(): OK
def open_edit_person_window(): ok

DIAGRAFH
def open_delete_person_window(): ok!
def open_delete_relationship_window(): OK

MENU

'''
    # ------------------ Δημιουργία ------------------

def open_add_person_window():
    """Δημιουργεί παράθυρο για την εισαγωγή νέου ατόμου."""
    add_window = Toplevel(root)
    add_window.title("Προσθήκη Ατόμου")
    add_window.geometry("350x300")

    Label(add_window, text="Όνομα:").pack()
    first_name_entry = Entry(add_window)
    first_name_entry.pack()

    Label(add_window, text="Επώνυμο:").pack()
    last_name_entry = Entry(add_window)
    last_name_entry.pack()

    Label(add_window, text="Ημερομηνία Γέννησης:").pack()
    birth_date_entry = Entry(add_window)
    birth_date_entry.pack()


    def save_person():
        """Αποθηκεύει το νέο άτομο στη βάση δεδομένων και εμφανίζει το ID του."""
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        birth_date = birth_date_entry.get()

        if first_name and last_name and birth_date:
            new_id = add_person(first_name, last_name, birth_date)  # Λήψη του νέου ID
            message = f"Δημιουργήθηκε προφίλ με ID {new_id} για τον χρήστη: {first_name} {last_name} με ημερομηνία γέννησης {birth_date}!"
            status_label.config(
                text=message,
                fg="green",
                font=("Arial", 12, "bold"),
                wraplength=300,  
                justify="center" 
            )
        else:
            status_label.config(text="Συμπληρώστε όλα τα πεδία!", fg="red")

    Button(add_window, text="Αποθήκευση", command=save_person).pack()
    status_label = Label(add_window, text="", fg="green")
    status_label.pack()




def open_add_relationship_window():
    """Δημιουργεί παράθυρο για προσθήκη σχέσης μεταξύ δύο ατόμων."""
    relationship_window = Toplevel(root)
    relationship_window.title("Προσθήκη Σχέσης")
    relationship_window.geometry("350x250")

    Label(relationship_window, text="ID Ατόμου 1:").pack()
    person1_entry = Entry(relationship_window)
    person1_entry.pack()

    Label(relationship_window, text="ID Ατόμου 2:").pack()
    person2_entry = Entry(relationship_window)
    person2_entry.pack()

    Label(relationship_window, text="Τύπος Σχέσης (parent, spouse, sibling, child):").pack()
    relation_type_entry = Entry(relationship_window)
    relation_type_entry.pack()

    def save_relationship():
        """Αποθηκεύει τη σχέση στη βάση δεδομένων και εμφανίζει το ID της."""
        person1_id = person1_entry.get()
        person2_id = person2_entry.get()
        relation_type = relation_type_entry.get()

        if person1_id.isdigit() and person2_id.isdigit() and relation_type in ['parent', 'spouse', 'sibling', 'child']:
            new_relation_id = add_relationship(person1_id, person2_id, relation_type)  # Λήψη του νέου ID σχέσης
            
            # Δημιουργία μηνύματος επιβεβαίωσης
            message = f"Δημιουργήθηκε η σχέση {relation_type} μεταξύ των ατόμων με ID {person1_id} και {person2_id}, με ID σχέσης {new_relation_id}!"

            status_label.config(
                text=message,
                fg="green",
                font=("Arial", 12),
                wraplength=300,  
                justify="center"
            )
        else:
            status_label.config(text="Μη έγκυρα δεδομένα!", fg="red", font=("Arial", 12, "bold"))

    Button(relationship_window, text="Αποθήκευση", command=save_relationship).pack()
    status_label = Label(relationship_window, text="", fg="green")
    status_label.pack()


    # ------------------ Επεξεργασία ------------------


from tkinter import *
from Database import get_person, update_person  # Εισάγουμε τις σωστές συναρτήσεις

def open_edit_person_window():
    """Δημιουργεί παράθυρο για επεξεργασία ατόμου."""
    edit_window = Toplevel(root)
    edit_window.title("Επεξεργασία Ατόμου")
    edit_window.geometry("350x350")

    Label(edit_window, text="ID ατόμου:").pack()
    id_entry = Entry(edit_window)
    id_entry.pack()

    def load_person():
        """Φορτώνει τα στοιχεία του ατόμου από τη βάση δεδομένων."""
        person_id = id_entry.get()
        
        if person_id.isdigit():  # Έλεγχος εγκυρότητας ID
            person = get_person(person_id)
            if person:
                first_name_entry.delete(0, END)
                last_name_entry.delete(0, END)
                birth_date_entry.delete(0, END)

                first_name_entry.insert(0, person[1])  # Προσαρμογή στη δομή της βάσης
                last_name_entry.insert(0, person[2])
                birth_date_entry.insert(0, person[3])
            else:
                status_label.config(text="Δεν βρέθηκε άτομο με αυτό το ID!", fg="red")
        else:
            status_label.config(text="Μη έγκυρο ID!", fg="red")

    Label(edit_window, text="Όνομα:").pack()
    first_name_entry = Entry(edit_window)
    first_name_entry.pack()

    Label(edit_window, text="Επώνυμο:").pack()
    last_name_entry = Entry(edit_window)
    last_name_entry.pack()

    Label(edit_window, text="Ημερομηνία Γέννησης:").pack()
    birth_date_entry = Entry(edit_window)
    birth_date_entry.pack()



    Button(edit_window, text="Φόρτωση Στοιχείων", command=load_person).pack()
    status_label = Label(edit_window, text="", fg="green")
    status_label.pack()

    def save_updated_person():
        """Ενημερώνει το άτομο στη βάση δεδομένων και εμφανίζει μήνυμα επιβεβαίωσης."""
        person_id = id_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        birth_date = birth_date_entry.get()

        if person_id.isdigit():
            update_person(person_id, first_name, last_name, birth_date)
            status_label.config(text=f"Το προφίλ με ID {person_id} ενημερώθηκε επιτυχώς!", fg="green", font=("Arial", 12))
        else:
            status_label.config(text="Μη έγκυρο ID!", fg="red", font=("Arial", 12, "bold"))

    Button(edit_window, text="Αποθήκευση Αλλαγών", command=save_updated_person).pack()




def open_edit_relationship_window():
    """Δημιουργεί παράθυρο για επεξεργασία σχέσης μεταξύ δύο ατόμων."""
    edit_window = Toplevel(root)
    edit_window.title("Επεξεργασία Σχέσης")
    edit_window.geometry("350x300")

    Label(edit_window, text="ID Σχέσης:").pack()
    relationship_id_entry = Entry(edit_window)
    relationship_id_entry.pack()

    def load_relationship():
        """Φορτώνει τα στοιχεία της σχέσης από τη βάση δεδομένων."""
        relationship_id = relationship_id_entry.get()

        if relationship_id.isdigit():
            relationship = get_relationship(relationship_id)
            if relationship:
                person1_entry.delete(0, END)
                person2_entry.delete(0, END)
                relation_type_entry.delete(0, END)

                person1_entry.insert(0, relationship[1])
                person2_entry.insert(0, relationship[2])
                relation_type_entry.insert(0, relationship[3])
            else:
                status_label.config(text="Δεν βρέθηκε η σχέση!", fg="red")
        else:
            status_label.config(text="Μη έγκυρο ID!", fg="red")

    Label(edit_window, text="ID Ατόμου 1:").pack()
    person1_entry = Entry(edit_window)
    person1_entry.pack()

    Label(edit_window, text="ID Ατόμου 2:").pack()
    person2_entry = Entry(edit_window)
    person2_entry.pack()

    Label(edit_window, text="Τύπος Σχέσης (parent, spouse, sibling, child):").pack()
    relation_type_entry = Entry(edit_window)
    relation_type_entry.pack()

    Button(edit_window, text="Φόρτωση Στοιχείων", command=load_relationship).pack()

    def save_updated_relationship():
        """Ενημερώνει τη σχέση στη βάση δεδομένων και εμφανίζει μήνυμα επιβεβαίωσης."""
        relationship_id = relationship_id_entry.get()
        new_type = relation_type_entry.get()

        if relationship_id.isdigit() and new_type in ['parent', 'spouse', 'sibling', 'child']:
            update_relationship_by_id(relationship_id, new_type)
            status_label.config(text=f"Η σχέση με ID {relationship_id} ενημερώθηκε σε '{new_type}'!", fg="green", font=("Arial", 12))
        else:
            status_label.config(text="Μη έγκυρα δεδομένα!", fg="red", font=("Arial", 12, "bold"))

    Button(edit_window, text="Αποθήκευση Αλλαγών", command=save_updated_relationship).pack()
    status_label = Label(edit_window, text="", fg="green")
    status_label.pack()


    # ------------------ Διαγραφή ------------------


def open_delete_person_window():
    """Δημιουργεί παράθυρο για διαγραφή ατόμου."""
    delete_window = Toplevel(root)
    delete_window.title("Διαγραφή Ατόμου")
    delete_window.geometry("350x300")

    Label(delete_window, text="ID ατόμου προς διαγραφή:").pack()
    id_entry = Entry(delete_window)
    id_entry.pack()

    person_details_label = Label(delete_window, text="", fg="black", font=("Arial", 11))
    person_details_label.pack()

    def load_person():
        """Φορτώνει και εμφανίζει τα στοιχεία του ατόμου πριν τη διαγραφή."""
        person_id = id_entry.get()

        if person_id.isdigit():
            person = get_person(person_id)
            if person:
                person_details_label.config(text=f"Όνομα: {person[1]}\nΕπώνυμο: {person[2]}\nΗμ/νία Γέννησης: {person[3]}", fg="black", font=("Arial", 11))
            else:
                person_details_label.config(text="Δεν βρέθηκε άτομο με αυτό το ID!", fg="red", font=("Arial", 11, "bold"))
        else:
            person_details_label.config(text="Μη έγκυρο ID!", fg="red", font=("Arial", 11, "bold"))

    Button(delete_window, text="Φόρτωση Στοιχείων", command=load_person).pack()

    def confirm_delete():
        """Διαγράφει το άτομο από τη βάση δεδομένων και εμφανίζει μήνυμα επιβεβαίωσης."""
        person_id = id_entry.get()

        if person_id.isdigit():
            delete_person(person_id)
            status_label.config(text=f"Το άτομο με ID {person_id} διαγράφηκε επιτυχώς!", fg="green", font=("Arial", 12))
        else:
            status_label.config(text="Μη έγκυρο ID!", fg="red", font=("Arial", 12, "bold"))

    Button(delete_window, text="Διαγραφή", command=confirm_delete).pack()
    status_label = Label(delete_window, text="", fg="green")
    status_label.pack()

def open_delete_relationship_window():
    """Δημιουργεί παράθυρο για διαγραφή σχέσης."""
    delete_window = Toplevel(root)
    delete_window.title("Διαγραφή Σχέσης")
    delete_window.geometry("350x300")

    Label(delete_window, text="ID Σχέσης προς διαγραφή:").pack()
    relationship_id_entry = Entry(delete_window)
    relationship_id_entry.pack()

    relationship_details_label = Label(delete_window, text="", fg="black", font=("Arial", 11))
    relationship_details_label.pack()

    def load_relationship():
        """Φορτώνει και εμφανίζει τα στοιχεία της σχέσης πριν τη διαγραφή."""
        relationship_id = relationship_id_entry.get()

        if relationship_id.isdigit():
            relationship = get_relationship(relationship_id)
            if relationship:
                relationship_details_label.config(
                    text=f"Ατόμο 1 ID: {relationship[1]}\nΑτόμο 2 ID: {relationship[2]}\nΤύπος Σχέσης: {relationship[3]}",
                    fg="black", font=("Arial", 11)
                )
            else:
                relationship_details_label.config(text="Δεν βρέθηκε σχέση με αυτό το ID!", fg="red", font=("Arial", 11, "bold"))
        else:
            relationship_details_label.config(text="Μη έγκυρο ID!", fg="red", font=("Arial", 11, "bold"))

    Button(delete_window, text="Φόρτωση Στοιχείων", command=load_relationship).pack()

    def confirm_delete():
        """Διαγράφει τη σχέση από τη βάση δεδομένων και εμφανίζει μήνυμα επιβεβαίωσης."""
        relationship_id = relationship_id_entry.get()

        if relationship_id.isdigit():
            delete_relationship(relationship_id)
            status_label.config(text=f"Η σχέση με ID {relationship_id} διαγράφηκε επιτυχώς!", fg="green", font=("Arial", 12))
        else:
            status_label.config(text="Μη έγκυρο ID!", fg="red", font=("Arial", 12, "bold"))

    Button(delete_window, text="Διαγραφή", command=confirm_delete).pack()
    status_label = Label(delete_window, text="", fg="green")
    status_label.pack()


    # ------------------ Menu ------------------


root=Tk()

root.title('Project 29')
root.geometry("700x500")
root.config(bg='#9fc5e8') 


def test():
    ''' to dhmiourgw gia na to vazooume gia command mexri na xtisoume to upoloipo'''
    print('test')


menu=Menu(root)
root.config(menu=menu)


bold_font = Font(family="Segoe UI", size=9) #weight="bold"
'''
arxeio= Menu(menu, tearoff=0)  #bg='#cfe2f3', activebackground='#b4a7d6', activeforeground='white')
menu.add_cascade(label='Αρχείο', menu=arxeio)
arxeio.add_command(label='Νέο Δέντρο', command= test, font=bold_font)
arxeio.add_command(label='Αποθήκευση', command= test)
arxeio.add_command(label='Έξοδος', command= root.destroy)

'''



profil= Menu(menu, tearoff=0)
menu.add_cascade(label='Προφίλ', menu=profil)
profil.add_command(label='Προσθήκη', command=open_add_person_window) 
profil.add_command(label='Επεξεργασία', command=open_edit_person_window) 
profil.add_command(label='Διαγραφή', command=open_delete_person_window) 



sxeseis= Menu(menu, tearoff=0)
menu.add_cascade(label='Σχέσεις', menu=sxeseis)
sxeseis.add_command(label='Προσθήκη', command=open_add_relationship_window) 
sxeseis.add_command(label='Επεξεργασία', command=open_edit_relationship_window)
sxeseis.add_command(label='Διαγραφή', command=open_delete_relationship_window) 





provoli= Menu(menu, tearoff=0)
menu.add_cascade(label='Προβολή', menu=provoli)
provoli.add_command(label='Εμφάνιση Δέντρου', command=test)



anazitisi= Menu(menu, tearoff=0)
menu.add_cascade(label='Αναζήτηση', menu=anazitisi)
anazitisi.add_command(label='Αναζήτηση Απογόνων', command=test) 


voitheia= Menu(menu, tearoff=0)
menu.add_cascade(label='Βοήθεια', menu=voitheia)
voitheia.add_command(label='Οδηγίες', command=test) 
voitheia.add_command(label='About us', command=test) 



root.mainloop()
