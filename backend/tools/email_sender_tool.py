import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
EMAIL_PASS = os.getenv("EMAIL_PASSWORD")

def send_email(to_mail:str, subject:str, body:str):
    msg = MIMEText(body)

    msg["Subject"]=subject
    msg["From"]=EMAIL
    msg["To"]=to_mail

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, EMAIL_PASS)
        server.send_message(msg)
    return "Email sent successfully to {to_mail}"

