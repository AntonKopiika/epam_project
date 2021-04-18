from src.models.department import Department
from src import db


def populate_departments():
    department_1 = Department("general management")
    department_2 = Department("marketing department")
    department_3 = Department("operations department")
    department_4 = Department("finance department")
    department_5 = Department("sales department")
    department_6 = Department("human resource department")
    department_7 = Department("purchase department")

    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)
    db.session.add(department_4)
    db.session.add(department_5)
    db.session.add(department_6)
    db.session.add(department_7)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    populate_departments()
    print("departments are populated!")
