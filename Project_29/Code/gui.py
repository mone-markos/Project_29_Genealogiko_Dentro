from tkinter import *
from tkinter.font import Font

from Database import *

from search_utility import *

from graph import *
import networkx as nx
import matplotlib.pyplot as plt
import tkinter.messagebox

'''
periexomena:

DHMIOURGIA
def open_add_person_window()
def open_add_relationship_window()

EPEKSERGASIA
def open_edit_relationship_window()
def open_edit_person_window()

DIAGRAFH
def open_delete_person_window()
def open_delete_relationship_window()

ANAZHTHSH APOGONWN
def open_search_descendants_window()

VOITHEIA
def show_profile_help()
def show_relationship_help()
def show_graph_help()
def show_search_help()

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
            new_id = add_person(first_name, last_name, birth_date)  
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

    Label(relationship_window, text="Τύπος Σχέσης:").pack()
    
    #dropdown menu
    relationship_types = ["parent(1)-child(2)", "spouse", "sibling"]
    selected_relationship = StringVar()
    selected_relationship.set(relationship_types[0])
    
    dropdown = OptionMenu(relationship_window, selected_relationship, *relationship_types)
    dropdown.pack()

    def save_relationship():
        """Αποθηκεύει τη σχέση στη βάση δεδομένων και εμφανίζει επιβεβαίωση."""
        person1_id = person1_entry.get()
        person2_id = person2_entry.get()
        relation_type = selected_relationship.get()  

#προσπαθούμε να παραβλέψουμε αυτό το πρόβλημα στην db με την αστοχία δύο τύπων σχέσεων για την σχέση parent-child: 

        if relation_type == "parent(1)-child(2)":
            relation_type = "parent"


            
        if person1_id.isdigit() and person2_id.isdigit():
            add_relationship(person1_id, person2_id, relation_type)

            display_type = "parent(1)-child(2)" if relation_type == "parent" else relation_type #τράμπα για το print
            
            status_label.config(text=f"Σχέση {display_type} αποθηκεύτηκε!", fg="green")
        else:
            status_label.config(text="Μη έγκυρα δεδομένα!", fg="red")

    Button(relationship_window, text="Αποθήκευση", command=save_relationship).pack()
    status_label = Label(relationship_window, text="", fg="green")
    status_label.pack()


    # ------------------ Επεξεργασία ------------------


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





def get_person_name(person_id):
    """Επιστρέφει το όνομα και το επώνυμο του ατόμου με βάση το ID."""
    conn = sqlite3.connect("family_tree.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT first_name, last_name FROM people WHERE id=?", (person_id,))
    person = cursor.fetchone()
    
    conn.close()
    return person if person else ("Άγνωστο", "Άγνωστο")

def open_edit_relationship_window():
    """Δημιουργεί παράθυρο για επεξεργασία σχέσης μεταξύ δύο ατόμων."""
    edit_window = Toplevel(root)
    edit_window.title("Επεξεργασία Σχέσης")
    edit_window.geometry("400x300")

    Label(edit_window, text="ID Σχέσης:").pack()
    relationship_id_entry = Entry(edit_window)
    relationship_id_entry.pack()

    person1_label = Label(edit_window, text="")  
    person1_label.pack()
    
    person2_label = Label(edit_window, text="")  
    person2_label.pack()

    current_relationship_label = Label(edit_window, text="")  
    current_relationship_label.pack()

    new_relationship_label = Label(edit_window, text="", fg="blue") 
    new_relationship_label.pack()

    relationship_types = ["parent(1)-child(2)", "spouse", "sibling"]
    selected_relationship = StringVar()
    selected_relationship.set(relationship_types[0])

    dropdown = OptionMenu(edit_window, selected_relationship, *relationship_types)
    dropdown.pack()

    def load_relationship():
        """Φορτώνει τα τρέχοντα δεδομένα της σχέσης από τη βάση."""
        relationship_id = relationship_id_entry.get()

        if relationship_id.isdigit():
            relationship = get_relationship(relationship_id)
            if relationship:
                person1_name = get_person_name(relationship[1])
                person2_name = get_person_name(relationship[2])         
#προσπαθούμε να παραβλέψουμε αυτό το πρόβλημα στην db με την αστοχία δύο τύπων σχέσεων για την σχέση parent-child: 
                displayed_relationship = "parent(1)-child(2)" if relationship[3] == "parent" else relationship[3]

                person1_label.config(text=f"ΑΤΟΜΟ 1: {relationship[1]} - {person1_name[0]} {person1_name[1]}")
                person2_label.config(text=f"ΑΤΟΜΟ 2: {relationship[2]} - {person2_name[0]} {person2_name[1]}")
                current_relationship_label.config(text=f"Τρέχων Τύπος Σχέσης: {displayed_relationship}")
                new_relationship_label.config(text="")  
            else:
                current_relationship_label.config(text="Δεν βρέθηκε η σχέση!", fg="red")
        else:
            current_relationship_label.config(text="Μη έγκυρο ID!", fg="red")


    def save_updated_relationship():
        """Αποθηκεύει τον νέο τύπο σχέσης στη βάση και τον εμφανίζει από κάτω."""
        relationship_id = relationship_id_entry.get()
        new_type = selected_relationship.get()


        if new_type == "parent(1)-child(2)":
            new_type = "parent"  #και πάλι, προσπαθούμε να παραβλέψουμε αυτό το πρόβλημα στην db

        allowed_types = {"parent", "spouse", "sibling", "child"}

        if relationship_id.isdigit() and new_type in allowed_types:
            update_relationship_by_id(relationship_id, new_type)
#Μετατροπή parent σε parent(1)-child(2) για την εμφάνιση σε μια τελευταία απεγνωσμένη τελευταία προσπάθεια
            display_type = "parent(1)-child(2)" if new_type == "parent" else new_type


            new_relationship_label.config(text=f"Νέος Τύπος Σχέσης: {display_type}", fg="blue")
        else:
            new_relationship_label.config(text="Μη έγκυρο ID!", fg="red")

    Button(edit_window, text="Φόρτωση Στοιχείων", command=load_relationship).pack()
    Button(edit_window, text="Αποθήκευση Αλλαγών", command=save_updated_relationship).pack()

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

    # ------------------ Αναζήτηση Απογόνων ------------------


def open_search_descendants_window():
    """Δημιουργεί παράθυρο για αναζήτηση απογόνων ενός ατόμου."""
    search_window = Toplevel(root)
    search_window.title("Αναζήτηση Απογόνων")
    search_window.geometry("400x300")

    Label(search_window, text="Εισάγετε ID Ατόμου:").pack()
    id_entry = Entry(search_window)
    id_entry.pack()

    result_listbox = Listbox(search_window, width=50, height=10)
    result_listbox.pack()

    def search_descendants():
        """Εκτελεί την αναζήτηση και εμφανίζει τους απογόνους στη λίστα."""
        person_id = id_entry.get()
        if not person_id.isdigit():
            result_listbox.insert(END, "Μη έγκυρο ID!")
            return

        descendants = find_descendants(int(person_id))  

        result_listbox.delete(0, END) 
        if descendants:
            for descendant in descendants:
                result_listbox.insert(END, f" (ID: {descendant['id']}) {descendant['first_name']} {descendant['last_name']}")
        else:
            result_listbox.insert(END, "Δεν βρέθηκαν απόγονοι.")

    Button(search_window, text="Αναζήτηση", command=search_descendants).pack()

    # ------------------ Βοήθεια ------------------
def show_profile_help():
    """Pop-up με οδηγίες για την προσθήκη προφίλ."""
    help_window = Toplevel(root)
    help_window.title("Βοήθεια - Προσθήκη Προφίλ")
    help_window.geometry("400x250")

    instructions = """Πώς να διαχειριστείτε ένα  προφίλ ατόμου:

- Προσθήκη: Συμπληρώστε όνομα, επώνυμο, ημερομηνία γέννησης.

- Επεξεργασία: Κάντε αναζήτηση μέσω του ID. Πατήστε "Φόρτωση Στοιχείων". Έπειτα μπορείτε να τροποποιήσετε τα στοιχεία ενός ατόμου, όπως όνομα, επώνυμο και ημερομηνία γέννησης. Τέλος, πατήστε "Αποθήκευση Αλλαγών".

- Διαγραφή: Κάντε αναζήτηση μέσω του ID. Πατήστε "Φόρτωση Στοιχείων" για επιβεβαίωση ότι είναι το σωστό προφίλ. Έπειτα μπορείτε να διαγράψετε το άτομο πατώντας διαγραφή."""

    Label(help_window, text=instructions, justify="left", wraplength=380).pack(pady=10)
    Button(help_window, text="Κλείσιμο", command=help_window.destroy).pack()
def show_relationship_help():
    """Εμφανίζει pop-up με οδηγίες για τις σχέσεις."""
    help_window = Toplevel(root)
    help_window.title("Βοήθεια - Σχέσεις")
    help_window.geometry("400x200")

    instructions = """Πώς να διαχειριστείτε τις σχέσεις:
    
- Προσθήκη: Επιλέξτε δύο άτομα μέσω του ID τους και καθορίστε τον τύπο σχέσης (γονιός (άτομο 1)-παιδί (άτομο 2), σύζυγοι, αδέλφια).

- Επεξεργασία: Αναζητήστε τη σχέση με το ID και τροποποιήστε τον τύπο της μέσω του drop down menu.

- Διαγραφή: Επιλέξτε τη σχέση με το ID. Πατήστε "Φόρτωση Στοιχείων" για επιβεβαίωση ότι είναι η σχέση που θέλετε να διαγράψετε. Έπειτα μπορείτε να διαγράψετε την σχέση πατώντας διαγραφή."""

    Label(help_window, text=instructions, justify="left", wraplength=380).pack(pady=10)
    Button(help_window, text="Κλείσιμο", command=help_window.destroy).pack()

def show_graph_help():
    """Pop-up με οδηγίες για τον γράφο."""
    help_window = Toplevel(root)
    help_window.title("Βοήθεια - Γράφος")
    help_window.geometry("400x200")

    instructions = """Πώς να χρησιμοποιήσετε τον γράφο:

Ο γράφος εμφανίζει τις σχέσεις μεταξύ ατόμων με συνδετικές γραμμές.

Κωδικοποίηση γραμμών:
  Κόκκινο: Σύζυγοι
  Μωβ: Γονιός-Παιδί
  Μπλε: Αδέρφια

Δοκιμάστε να κάνετε κλικ σε έναν κόμβο (άτομο) για περισσότερες πληροφορίες."""

    Label(help_window, text=instructions, justify="left", wraplength=380).pack(pady=10)
  
def show_search_help():
    """Pop-up με οδηγίες για την αναζήτηση απογόνων."""
    help_window = Toplevel(root)
    help_window.title("Βοήθεια - Αναζήτηση Απογόνων")
    help_window.geometry("400x250")

    instructions = """Πώς να αναζητήσετε απογόνους:

Επιλέξτε ένα άτομο με την εισαγωγή του ID του. Το πρόγραμμα επιστρέφει.

Η εφαρμογή θα διασχίσει τις σχέσεις αυτού του ατόμου για να βρει όλους τους απογόνους και θα εμφανιστεί λίστα με τους απογόνους κάθε επιπέδου.

Σημείωση: Η αναζήτηση συνεχίζεται μέχρι το τελευταίο άτομο στο μονοπάτι."""

    Label(help_window, text=instructions, justify="left", wraplength=380).pack(pady=10)
    Button(help_window, text="Κλείσιμο", command=help_window.destroy).pack()




    # ------------------ Menu ------------------


root=Tk()

root.title('Project 29')
root.geometry("400x20")
root.config(bg='#9fc5e8') 


def test():
    ''' to dhmiourgw gia na to vazooume gia command mexri na xtisoume to upoloipo'''
    print('test')


menu=Menu(root)
root.config(menu=menu)


bold_font = Font(family="Segoe UI", size=9)




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
provoli.add_command(label='Εμφάνιση Δέντρου', command=display_family_tree)



anazitisi= Menu(menu, tearoff=0)
menu.add_cascade(label='Αναζήτηση', menu=anazitisi)
anazitisi.add_command(label='Αναζήτηση Απογόνων', command=open_search_descendants_window) 


voitheia= Menu(menu, tearoff=0)
menu.add_cascade(label='Βοήθεια', menu=voitheia)
voitheia.add_command(label='Προφίλ', command=show_profile_help) 
voitheia.add_command(label='Σχέσεις', command=show_relationship_help) 
voitheia.add_command(label='Γράφος', command=show_graph_help)
voitheia.add_command(label='Αναζήτηση', command=show_search_help)



eksodos= Menu(menu, tearoff=0)  #bg='#cfe2f3', activebackground='#b4a7d6', activeforeground='white'
menu.add_cascade(label='Έξοδος', menu=eksodos) 
eksodos.add_command(label='Έξοδος', command= root.destroy)



root.mainloop()
