from datetime import datetime

from flask_restful import Resource
import src.service.database_queries as service


class Statistics(Resource):
    def get(self, uuid):
        department = service.get_department_by_uuid(uuid)
        if department:
            employees = department.employees
            if employees:
                salary_list = [employee.salary for employee in employees]
                avg_salary = sum(salary_list) / len(employees)
                max_salary = max(salary_list)
                min_salary = min(salary_list)
                birthday_list = [employee.birthday for employee in employees]
                min_birthday = datetime.strftime(max(birthday_list), '%Y-%m-%d')
                max_birthday = datetime.strftime(min(birthday_list), '%Y-%m-%d')
                return {"employees": len(employees), "avg_salary": avg_salary, "max_salary": max_salary,
                        "min_salary": min_salary, "min_birthday": min_birthday, "max_birthday": max_birthday}, 200
            return {"employees": 0}, 200
        return "", 404
