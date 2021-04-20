import smtplib
from email.message import EmailMessage
from config import Config
from password_utils import random_password


def send_password(receiver: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = "[No reply] your employee password"
    msg["From"] = Config.EMAIL_ADDRES
    msg["To"] = receiver
    msg.set_content(
        f"Congratulations, you are registered as an employee with password: {random_password()}. You can change your "
        f"password after first login to system."
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(Config.EMAIL_ADDRES, Config.EMAIL_PASSWORD)
        smtp.send_message(msg)
