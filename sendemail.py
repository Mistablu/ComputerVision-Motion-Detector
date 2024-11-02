import smtplib, ssl
import os
def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "greatkahlee@gmail.com"
    password = os.getenv("PASSWORD")

    sslcontext = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=sslcontext) as server:
        server.login(username,password)
        server.sendmail(username, username, message)