# prepei na yparxei kati poy "antikatoptrizei" to database
from app import App
from datetime import date
from person import Person
def main():
    app = App()

    # app.create_new_person('Maria','Kanakh', date(1985, 5, 15))
    # app.create_new_person("Bob", "Smith", date(1982, 8, 20))
    # p1 = app.find_person(id=1)
    # p2 = app.find_person(id=2)
    # app.add_spouse_relationship(p1, p2)

    # print(p1.spouse.name, p2.spouse.name)

    # ftiakse ena kainoyrio person, ton giannh
    # kanton paidi toy Bob (aftomata tha ginei kai ths marias)
    
    # app.create_new_person('John', 'Smith', date(2005, 3, 20))
    # app.add_parent_relationship(bob, John)
    # app.create_new_person('John', 'Sandy', date(2002, 3, 20))
    bob = app.find_person(id=2)
    John = app.find_person(name="John")

    # app.update_person(John, new_name=John.name, new_last_name="Allo", new_date_of_birth=date(1990, 10, 1))
    # app.add_parent_relationship(bob, John)
    # kai meta dokimase na to vreis sthn vash

    # print(app.find_relationship(bob, John))
    # person = app.find_person(id=1)
    # app.db.delete_all_relationship_of_person_id(3)
    # app.delete_person(id=John.id)
    # print(person.date_of_birth)

    person = app.find_person(name="John", last_name="Smith")

    if person:
        print(person.last_name, person.id)

    person = app.find_person(name="John", last_name="Allo")

    if person:
        print(person.last_name, person.id)

    # for person in app.find_people(name="John"):
    #     print(person.id)

if __name__ == "__main__":
    main()