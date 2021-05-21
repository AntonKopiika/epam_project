"""
This module implements sending emails using mailgun service
"""
import requests
import os


def send_password(receiver: str, password: str):
    return requests.post(
        f"https://api.mailgun.net/v3/{os.environ['MAILGUN_DOMAIN']}/messages",
        auth=("api", os.environ["MAILGUN_API_KEY"]),
        data={"from": f"Departments admin <departments@{os.environ['MAILGUN_DOMAIN']}>",
              "to": [receiver],
              "subject": "[No reply] your employee password",
              "text": f"Congratulations, you are registered as an employee with password: {password}. You can change "
                      f"your password after first login to system."})
