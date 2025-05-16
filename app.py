from person import Person
from database import Database
from typing import List

class App:
    def __init__(self):
        self.db = Database()
        self.people : List[Person] = self.db.get_all_people() # diavazei apthn vash oloys toys anthrwpoys
   
    # PROSOXH: an to name den einai None kai to min_date_of_birth den einai None, prepei na filtrareis me vash kai ta dyo!
    # mporeis na epistrefeis mono ena Person, to prwto poy tha vreis me afta ta krithria
    def find_person(self, id=None, name=None, last_name=None, min_date_of_birth=None, max_date_of_birth=None):
        people = self.find_people(id, name, last_name, min_date_of_birth, max_date_of_birth)

        if people:
            return people[0]
        
        return None
    
    def find_people(self, id=None, name=None, last_name=None, min_date_of_birth=None, max_date_of_birth=None):
        people = []
        for person in self.people:
            if        (person.name == name or name is None) \
                    and (person.last_name == last_name or last_name is None) \
                    and (min_date_of_birth is not None and person.date_of_birth >= min_date_of_birth or min_date_of_birth is None) \
                    and (person.id == id or id is None) \
                    and (max_date_of_birth is not None and person.date_of_birth <= max_date_of_birth or max_date_of_birth is None):

                people.append(person)
        
        return people

    def create_new_person(self, name, last_name, date_of_birth):
        id = self.db.insert_person(name, last_name, date_of_birth)
        p = Person(id, name, last_name, date_of_birth)
        self.people.append(p)
        return p
    
    def delete_person(self, id=None):
        if id is None:
            return
        
        # estw id = 3

        # theloyme oxi mono na diagrapsoyme to person alla kai oles tis sxeseis poy exei

        # stoxos:
        # 1. na vgei to antikeimeno apthn lista
        # diafora pop me remove:
        # pop: diagrafw kati se mia sygkekrimenh thesh
        # remove: diagrafw ena sygkekrimeno antikeimeno (to prwto)
        person = self.find_person(id)

        self.people.remove(person)

        # 2. na diagraftei to person apto table people
        self.db.delete_person(id)

        # 3. na diagraftoyn oles oi sxeseis stis opoies yparxei to id toy person
        # den xreiazetai! logw toy cascade. <3 sqlite
        self.db.delete_all_relationship_of_person_id(id)
        
    # p1 (kai spouse toy p1) einai parent toy p2
    def add_parent_relationship(self, p1, p2):
        self.db.insert_relationship(p1.id, p2.id, 'parent')
        p1.children.append(p2)
        if p1.spouse is not None:
            self.db.insert_relationship(p1.spouse.id, p2.id, 'parent') 
            p1.spouse.children.append(p2)

    def add_spouse_relationship(self, p1, p2):
        self.db.insert_relationship(p1.id, p2.id, 'spouse')
        p1.spouse = p2
        p2.spouse = p1
    
    
    # epistrefei: spouse, parent, child, grandparent, grandchild, sibling, cousin, aunt, other
    # h sxesei toy p1 ws pros to p2
    def find_relationship(self, p1 : Person, p2 : Person):
        if p1.spouse == p2:
            return 'spouse'
        
        if p1 in p2.parents:
            return 'parent'
        
        if p2 in p1.parents:
            return 'child'
        

        # Grandparent
        for p1_child in p1.children:
            if p2 in p1_child.children:
                return 'grandparent'

        # Grandchild
        for p1_parent in p1.parents:
            if p2 in p1_parent.parents:
                return 'grandchild'

        # Sibling
        for p1_parent in p1.parents:
            for p2_parent in p2.parents:
                if p1_parent == p2_parent and p1 != p2:
                    return 'sibling'
                
        # Aunt (P1 is aunt of P2)
        for p2_parent in p2.parents:
            for p1_parent_of_aunt_uncle in p1.parents:
                 for p2_parent_of_parent in p2_parent.parents:
                     if p1_parent_of_aunt_uncle == p2_parent_of_parent and p1 != p2_parent:
                         return 'aunt'
                     
        # Cousin (P1 and P2 are cousins)
        for p1_parent in p1.parents:
            for p2_parent in p2.parents:
                for p1_grandparent in p1_parent.parents:
                    for p2_grandparent in p2_parent.parents:
                        if p1_grandparent == p2_grandparent and p1_parent != p2_parent:
                             return 'cousin'
                        
        # Other (None of the above)
        return 'other'
        
    
    # update person details
    # dinoyme to person poy theloyme na allaksoyme (to antikeimeno apo thn lista)
    def update_person(self, p1, new_name, new_last_name, new_date_of_birth):
        p1.name = new_name
        p1.last_name = new_last_name
        p1.date_of_birth = new_date_of_birth
        if id is not None:
            self.db.update_person(p1.id, new_name, new_last_name, new_date_of_birth)