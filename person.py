class Person:
    def __init__(self, id, name, last_name, date_of_birth):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        
        # kena relationships sthn arxh
        self.spouse = None # o syzhgos san Person
        self.children = [] # lista me antikeimena Person
        self.parents = []
    
    def print_details(self):
        print(f'id: {self.id}, name: {self.name}, last name: {self.last_name}, dob: {self.date_of_birth}')