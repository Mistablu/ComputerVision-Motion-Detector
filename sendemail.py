import smtplib, ssl
import os
from email.message import EmailMessage

def send_email(imagepath):
    host = "smtp.gmail.com"
    port = 465

    username = "greatkahlee@gmail.com"
    password = os.getenv("PASSWORD")

    sslcontext = ssl.create_default_context()

    email_message = EmailMessage()
    email_message["Subject"] = "Motion Detected!"
    email_message.set_content("New motion detected by camera")

    with open(imagepath,"rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype="png")


    with smtplib.SMTP_SSL(host, port, context=sslcontext) as server:
        server.login(username,password)
        server.sendmail(username, username, email_message.as_string())