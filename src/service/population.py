from datetime import date

from src.models.department import Department
from src.models.employee import Employee
from src import db


def populate():
    department_1 = Department("general management")
    department_2 = Department("marketing department")
    department_3 = Department("operations department")
    department_4 = Department("finance department")
    department_5 = Department("sales department")
    department_6 = Department("human resource department")
    department_7 = Department("purchase department")
    department_8 = Department("IT department")

    employee1 = Employee(first_name="Anton", last_name="Kopiika", position="Junior Python Developer", salary=600,
                         birthday=date(1999, 4, 2))
    employee2 = Employee(first_name="Dmytro", last_name="Ivanov", position="Junior Python Developer", salary=600,
                         birthday=date(2000, 1, 1))
    employee3 = Employee(first_name="Ihor", last_name="Salo", position="Middle Python Developer", salary=1500,
                         birthday=date(1996, 6, 6))
    employee4 = Employee(first_name="Yurii", last_name="Morozov", position="Middle Python Developer", salary=2000,
                         birthday=date(1997, 12, 20))
    employee5 = Employee(first_name="Petro", last_name="Mogula", position="Senior Python Developer", salary=3000,
                         birthday=date(1995, 9, 24))
    employee6 = Employee(first_name="Mykola", last_name="Zerov", position="HR", salary=1000,
                         birthday=date(1993, 8, 12))
    employee7 = Employee(first_name="Serhiy", last_name="Burbas", position="Frontend Developer", salary=800,
                         birthday=date(1998, 3, 7))

    department_8.employees = [employee1, employee2, employee3, employee4, employee5, employee7]
    department_6.employees = [employee6]

    db.session.add(department_1)
    db.session.add(department_2)
    db.session.add(department_3)
    db.session.add(department_4)
    db.session.add(department_5)
    db.session.add(department_6)
    db.session.add(department_7)

    db.session.add(employee1)
    db.session.add(employee2)
    db.session.add(employee3)
    db.session.add(employee4)
    db.session.add(employee5)
    db.session.add(employee6)
    db.session.add(employee7)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    db.session.query(Department).delete()
    db.session.query(Employee).delete()
    populate()
    print("employees are populated!")

    # populate_departments()
    # print("departments are populated!")
