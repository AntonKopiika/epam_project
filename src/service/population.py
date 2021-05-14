"""
This module stands for populating database
"""
from datetime import date
from src.models.department import Department
from src.models.employee import Employee
from src import db


def populate():
    """
    populating method for adding employees and departments to db
    """
    department_1 = Department("general management")
    department_2 = Department("marketing department")
    department_3 = Department("finance department")
    department_4 = Department("human resource department")
    department_5 = Department("IT department")

    employee1_1 = Employee(first_name="Maja", last_name="Tate", position="Head manager", salary=5000,
                           birthday=date(1984, 3, 9), is_admin=True, email="test1_1@mail.ru", password="test")
    employee1_2 = Employee(first_name="Itan", last_name="Tate", position="Head manager", salary=5000,
                           birthday=date(1981, 10, 29), is_admin=True, email="test1_2@mail.ru", password="test")
    employee1_3 = Employee(first_name="John", last_name="Evans", position="CEO", salary=10000,
                           birthday=date(1974, 5, 19), is_admin=True, email="test1_3@mail.ru", password="test")
    employee1_4 = Employee(first_name="Leroy", last_name="Mata", position="Deputy head manager", salary=4500,
                           birthday=date(1991, 11, 26), is_admin=False, email="test1_4@mail.ru", password="test")
    employee1_5 = Employee(first_name="Martha", last_name="Fleming", position="Deputy head manager", salary=4500,
                           birthday=date(1986, 8, 27), is_admin=False, email="test1_5@mail.ru", password="test")

    employee2_1 = Employee(first_name="Edward", last_name="Cake", position="Marketing manager", salary=4000,
                           birthday=date(1983, 11, 9), email="test2_1@mail.ru", password="test")
    employee2_2 = Employee(first_name="John", last_name="Stewart", position="Marketer", salary=1500,
                           birthday=date(1981, 6, 14), email="test2_2@mail.ru", password="test")
    employee2_3 = Employee(first_name="Emma", last_name="Pears", position="Marketer", salary=1500,
                           birthday=date(1994, 1, 9), email="test2_3@mail.ru", password="test")
    employee2_4 = Employee(first_name="Kenny", last_name="Lee", position="Marketer", salary=1500,
                           birthday=date(1997, 2, 25), email="test2_4@mail.ru", password="test")
    employee2_5 = Employee(first_name="Jill", last_name="Garcia", position="Secretary", salary=800,
                           birthday=date(1999, 7, 7), email="test2_5@mail.ru", password="test")

    employee3_1 = Employee(first_name="Neal", last_name="Riddle", position="Finance manager", salary=4000,
                           birthday=date(1980, 10, 30), email="test3_1@mail.ru", password="test")
    employee3_2 = Employee(first_name="John", last_name="Sampson", position="Accountant", salary=1500,
                           birthday=date(1985, 8, 1), email="test3_2@mail.ru", password="test")
    employee3_3 = Employee(first_name="Joan", last_name="Key", position="Accountant", salary=1500,
                           birthday=date(1978, 7, 16), email="test3_3@mail.ru", password="test")
    employee3_4 = Employee(first_name="Angela", last_name="Mcmahon", position="Accountant", salary=1500,
                           birthday=date(1991, 4, 24), email="test3_4@mail.ru", password="test")
    employee3_5 = Employee(first_name="Darrell", last_name="Farrington", position="Secretary", salary=800,
                           birthday=date(1997, 12, 5), email="test3_5@mail.ru", password="test")

    employee4_1 = Employee(first_name="Mykola", last_name="Zerov", position="Head HR", salary=2000,
                           birthday=date(1991, 9, 22), email="test4_1@mail.ru", password="test")
    employee4_2 = Employee(first_name="Irma", last_name="Klepko", position="HR", salary=1000,
                           birthday=date(1993, 8, 12), email="test4_2@mail.ru", password="test")
    employee4_3 = Employee(first_name="Yana", last_name="Zayceva", position="HR", salary=1000,
                           birthday=date(1995, 4, 7), email="test4_3@mail.ru", password="test")

    employee5_1 = Employee(first_name="Anton", last_name="Kopiika", position="Junior Python Developer", salary=600,
                           birthday=date(1999, 4, 2), is_admin=True, email="anton@mail.ru", password="12345678")
    employee5_2 = Employee(first_name="Dmytro", last_name="Ivanov", position="Junior Python Developer", salary=600,
                           birthday=date(2000, 1, 1), email="test5_1@mail.ru", password="test")
    employee5_3 = Employee(first_name="Ihor", last_name="Salo", position="Middle Python Developer", salary=1500,
                           birthday=date(1996, 6, 6), email="test5_2@mail.ru", password="test")
    employee5_4 = Employee(first_name="Yurii", last_name="Morozov", position="Middle Python Developer", salary=2000,
                           birthday=date(1997, 12, 20), email="test5_3@mail.ru", password="test")
    employee5_5 = Employee(first_name="Petro", last_name="Mogula", position="Senior Python Developer", salary=3000,
                           birthday=date(1995, 9, 24), email="test5_4@mail.ru", password="test")
    employee5_6 = Employee(first_name="Serhiy", last_name="Burbas", position="Frontend Developer", salary=800,
                           birthday=date(1998, 3, 7), email="test5_6@mail.ru", password="test")

    department_1.employees = [employee1_1, employee1_2, employee1_3, employee1_4, employee1_5]
    department_2.employees = [employee2_1, employee2_2, employee2_3, employee2_4, employee2_5]
    department_3.employees = [employee3_1, employee3_2, employee3_3, employee3_4, employee3_5]
    department_4.employees = [employee4_1, employee4_2, employee4_3]
    department_5.employees = [employee5_1, employee5_2, employee5_3, employee5_4, employee5_5, employee5_6]

    departments = [department_1, department_2, department_3, department_4, department_5]
    for department in departments:
        db.session.add(department)

    employees = [employee1_1, employee1_2, employee1_3, employee1_4, employee1_5, employee2_1, employee2_2, employee2_3,
                 employee2_4, employee2_5, employee3_1, employee3_2, employee3_3, employee3_4, employee3_5, employee4_1,
                 employee4_2, employee4_3, employee5_1, employee5_2, employee5_3, employee5_4, employee5_5, employee5_6]
    for employee in employees:
        db.session.add(employee)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    db.session.query(Department).delete()
    db.session.query(Employee).delete()
    populate()
    print("employees are populated!")
