import Database as db
from person import Person

# Επιστρέφει None αν δεν βρεί κάτι
def find_person(id=None, first_name=None, last_name=None, date_of_birth = None):
    people = find_people(id, first_name, last_name, date_of_birth)

    if people:
        return people[0]
    
    return None

# Επιστρέφει: [{'id':1, 'first_name':..., ...}, ..]
def find_people(id=None, first_name=None, last_name=None, date_of_birth = None):
    people = []
    for person in _get_all_people():
        if        (person.first_name == first_name or first_name is None) \
                and (person.last_name == last_name or last_name is None) \
                and (person.id == id or id is None) \
                and (person.date_of_birth == date_of_birth or date_of_birth is None):
            people.append(person)
    
    people_dicts = [person.as_dictionary() for person in people]

    return people_dicts

def find_relationship(id1, id2):
    all_people = _get_all_people()

    person1 = None 
    for p in all_people:
        if p.id == id1:
            person1 = p
            break 

    person2 = None 
    for p in all_people:
        if p.id == id2:
            person2 = p
            break 
    
    if person1 is None or person2 is None:
        return None

    return _find_relationship(person1, person2)


# Συνάρτηση που χρησιμοποιώ για να φτιάξω μια λίστα με όλα τα person ως αντικείμενα Person, μαζί με τις σχέσεις τους
def _get_all_people():
    sql = "SELECT * FROM people;"
    cursor = db.connect_db().cursor()

    cursor.execute(sql)
    
    people = []
    people_sql = cursor.fetchall()

    for person_sql in people_sql:
        people.append(Person(id=person_sql[0], first_name=person_sql[1], last_name=person_sql[2], date_of_birth=person_sql[3]))
    
    sql = "SELECT * FROM relationships;"
    cursor.execute(sql)
    relationships_sql = cursor.fetchall()

    # Φτιάχνω πρώτα συζήγους
    for relationship in relationships_sql:
        id1 = relationship[1]
        id2 = relationship[2]
        relationship_type = relationship[3]

        # Πρέπει στην λίστα το person με id1 να έχει spouse το person με id2 και τα παιδία του id1 να έχουν γόνεις το id1 και το id2 και αντίστροφα
        for person in people:
            if person.id == id1:
                person1 = person
                break 

        for person in people:
            if person.id == id2:
                person2 = person
                break 

        if relationship_type == 'spouse':
            person1.spouse = person2 
            person2.spouse = person1
        elif relationship_type == 'parent':
            person1.children.append(person2)
            person2.parents.append(person1)

    return people

def _find_relationship(p1 : Person, p2 : Person):
    if p1.spouse == p2:
        return 'spouse'
    
    if p1 in p2.parents:
        return 'parent'
    
    if p2 in p1.parents:
        return 'child'
    
        # Αδέρφια (P1 και P2 είναι αδέρφια)
    for p1_parent in p1.parents:
        for p2_parent in p2.parents:
            if p1_parent == p2_parent and p1 != p2:
                return 'sibling'

    return None

def find_descendants(person_id):
    all_people = _get_all_people()

    first_person = None
    for p in all_people:
        if p.id == person_id:
            first_person = p
            break

    if not first_person:
        return []
    
    descendants = []
    
    # Για αποφυγή διπλότυπων απογόνων
    visited_people = set()

    def _get_children(person):
        if person.id in visited_people:
            return
        visited_people.add(person.id)

        # Αναδρομηκή συνάρτηση που ψάχνει απογόνους και τους βάζει σε μια λίστα 
        for child in person.children:
            descendants.append(child.as_dictionary())
            _get_children(child)

    _get_children(first_person)
    return descendants