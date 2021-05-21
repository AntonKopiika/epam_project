"""
This module implements response for statistic requests
"""
from datetime import datetime
from flask_restful import Resource
import src.service.database_queries as service
from src.rest.resources.wrappers import check_authorisation


class Statistics(Resource):
    """
    Class for statistic restfull resource
    """
    @check_authorisation
    def get(self, uuid):
        """
        get method for statistics request
        :param uuid: department uuid
        :return: statistics of department in json, if such department exists
        """
        department = service.get_department_by_uuid(uuid)
        if department:
            employees = department.employees
            if employees:
                salary_list = [employee.salary for employee in employees]
                avg_salary = round(sum(salary_list) / len(employees),2)
                max_salary = max(salary_list)
                min_salary = min(salary_list)
                birthday_list = [employee.birthday for employee in employees]
                min_birthday = datetime.strftime(max(birthday_list), '%Y-%m-%d')
                max_birthday = datetime.strftime(min(birthday_list), '%Y-%m-%d')
                return {"employees": len(employees), "avg_salary": avg_salary, "max_salary": max_salary,
                        "min_salary": min_salary, "min_birthday": min_birthday, "max_birthday": max_birthday}, 200
            return {"employees": 0}, 200
        return "", 404
