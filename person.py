class Person:
    def __init__(self, id, first_name, last_name, date_of_birth):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        
        # Κενά relationships στην αρχή
        self.spouse = None
        self.children = [] 
        self.parents = []
    
    def as_dictionary(self):
        return {'id': self.id, 'first_name':self.first_name, 'last_name':self.last_name, 'birth_date': self.date_of_birth}