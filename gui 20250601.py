from tkinter import *
from tkinter.font import Font
import Database

'''
periexomena:

DHMIOURGIA
def open_add_person_window(): OK
def open_add_relationship_window(): OK

EPEKSERGASIA
def open_edit_relationship_window(): OK
def open_edit_person_window(): -

DIAGRAFH
def open_delete_person_window(): den diagrafontai oi sxeseis tou atomou pou diagrafetai
def open_delete_relationship_window(): OK

MENU

'''
    # ------------------ Δημιουργία ------------------

def open_add_person_window():
    """Δημιουργεί παράθυρο για την εισαγωγή νέου ατόμου."""
    add_window = Toplevel(root)
    add_window.title("Προσθήκη Ατόμου")
    add_window.geometry("300x250")

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
        """Αποθηκεύει το νέο άτομο στη βάση δεδομένων."""
        Database.add_person(
            first_name_entry.get(), 
            last_name_entry.get(), 
            birth_date_entry.get(),
        )
        status_label.config(text="Το άτομο προστέθηκε επιτυχώς!")

    Button(add_window, text="Αποθήκευση", command=save_person).pack()

    status_label = Label(add_window, text="", fg="green")
    status_label.pack()





def open_add_relationship_window():
    """Δημιουργεί παράθυρο για προσθήκη σχέσης μεταξύ δύο ατόμων."""
    relationship_window = Toplevel(root)
    relationship_window.title("Προσθήκη Σχέσης")
    relationship_window.geometry("300x250")

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
        """Αποθηκεύει τη σχέση στη βάση δεδομένων."""
        Database.add_relationship(
            person1_entry.get(),
            person2_entry.get(),
            relation_type_entry.get()
        )
        status_label.config(text="Η σχέση προστέθηκε επιτυχώς!", fg="green")

    Button(relationship_window, text="Αποθήκευση", command=save_relationship).pack()
    status_label = Label(relationship_window, text="", fg="green")
    status_label.pack()


    # ------------------ Επεξεργασία ------------------



def open_edit_person_window():
    """Δημιουργεί παράθυρο για επεξεργασία ατόμου."""
    edit_window = Toplevel(root)
    edit_window.title("Επεξεργασία Ατόμου")
    edit_window.geometry("300x300")

    Label(edit_window, text="ID ατόμου:").pack()
    id_entry = Entry(edit_window)
    id_entry.pack()

    def load_person():
        """Φορτώνει τα στοιχεία του ατόμου από τη βάση δεδομένων."""
        person_id = id_entry.get()
        person = Database.get_person(person_id)

        if person:
            first_name_entry.delete(0, END)
            last_name_entry.delete(0, END)
            birth_date_entry.delete(0, END)
            
            first_name_entry.insert(0, person.first_name)
            last_name_entry.insert(0, person.last_name)
            birth_date_entry.insert(0, person.date_of_birth.isoformat())
        else:
            status_label.config(text="Δεν βρέθηκε το άτομο!", fg="red")

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
        """Ενημερώνει το άτομο στη βάση δεδομένων."""
        Database.update_person(
        id_entry.get(), 
        first_name_entry.get(), 
        last_name_entry.get(), 
        birth_date_entry.get() 
    )
    status_label.config(text="Οι αλλαγές αποθηκεύτηκαν!", fg="green")

    Button(edit_window, text="Αποθήκευση Αλλαγών", command=save_updated_person).pack()



def open_edit_relationship_window():
    """Δημιουργεί παράθυρο για επεξεργασία σχέσης μεταξύ δύο ατόμων."""
    edit_window = Toplevel(root)
    edit_window.title("Επεξεργασία Σχέσης")
    edit_window.geometry("300x250")

    Label(edit_window, text="ID Σχέσης:").pack()
    relationship_id_entry = Entry(edit_window)
    relationship_id_entry.pack()

    def load_relationship():
        """Φορτώνει τα στοιχεία της σχέσης από τη βάση δεδομένων."""
        relationship_id = relationship_id_entry.get()
        relationship = Database.get_relationship(relationship_id)
        
        if relationship:
            person1_entry.delete(0, END)
            person2_entry.delete(0, END)
            relation_type_entry.delete(0, END)

            person1_entry.insert(0, relationship[1])
            person2_entry.insert(0, relationship[2])
            relation_type_entry.insert(0, relationship[3])
        else:
            status_label.config(text="Δεν βρέθηκε η σχέση!", fg="red")

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
        """Ενημερώνει τη σχέση στη βάση δεδομένων."""
        relationship_id = relationship_id_entry.get()
        new_type = relation_type_entry.get()

        if relationship_id.isdigit() and new_type in ['parent', 'spouse']:
            Database.update_relationship_by_id(relationship_id, new_type)
            status_label.config(text="Οι αλλαγές αποθηκεύτηκαν!", fg="green")
        else:
            status_label.config(text="Μη έγκυρα δεδομένα!", fg="red")

    Button(edit_window, text="Αποθήκευση Αλλαγών", command=save_updated_relationship).pack()

    status_label = Label(edit_window, text="", fg="green")
    status_label.pack()


    # ------------------ Διαγραφή ------------------


def open_delete_person_window():
    """Δημιουργεί παράθυρο για διαγραφή ατόμου."""
    delete_window = Toplevel(root)
    delete_window.title("Διαγραφή Ατόμου")
    delete_window.geometry("300x200")

    Label(delete_window, text="ID ατόμου προς διαγραφή:").pack()
    id_entry = Entry(delete_window)
    id_entry.pack()

    def confirm_delete():
        """Διαγράφει το άτομο από τη βάση δεδομένων."""
        person_id = id_entry.get()

        if person_id.isdigit():  
            Database.delete_person(person_id)
            status_label.config(text="Το άτομο διαγράφηκε!", fg="green")
        else:
            status_label.config(text="Μη έγκυρο ID!", fg="red")

    Button(delete_window, text="Διαγραφή", command=confirm_delete).pack()
    status_label = Label(delete_window, text="", fg="green")
    status_label.pack()




def open_delete_relationship_window():
    """Δημιουργεί παράθυρο για διαγραφή σχέσης."""
    delete_window = Toplevel(root)
    delete_window.title("Διαγραφή Σχέσης")
    delete_window.geometry("300x200")

    Label(delete_window, text="ID Σχέσης προς διαγραφή:").pack()
    relationship_id_entry = Entry(delete_window)
    relationship_id_entry.pack()

    def confirm_delete():

        """Διαγράφει τη σχέση από τη βάση δεδομένων."""
        relationship_id = relationship_id_entry.get()

        if relationship_id.isdigit():  # Έλεγχος εγκυρότητας ID
            Database.delete_relationship_by_id(relationship_id)
            status_label.config(text="Η σχέση διαγράφηκε!", fg="green")
        else:
            status_label.config(text="Μη έγκυρο ID!", fg="red")


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

arxeio= Menu(menu, tearoff=0)  #bg='#cfe2f3', activebackground='#b4a7d6', activeforeground='white')
menu.add_cascade(label='Αρχείο', menu=arxeio)
arxeio.add_command(label='Νέο Δέντρο', command= test, font=bold_font)
arxeio.add_command(label='Αποθήκευση', command= test)
arxeio.add_command(label='Έξοδος', command= root.destroy)





profil= Menu(menu, tearoff=0)
menu.add_cascade(label='Προφίλ', menu=profil)
profil.add_command(label='Προσθήκη', command=open_add_person_window) 
profil.add_command(label='Επεξεργασία', command=open_edit_person_window) 
profil.add_command(label='Διαγραφή', command=open_delete_person_window) 



sxeseis= Menu(menu, tearoff=0)
menu.add_cascade(label='Σχέσεις', menu=sxeseis)
sxeseis.add_command(label='Πρσθήκη', command=open_add_relationship_window) 
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
