import smtplib
from email.mime.text import MIMEText
from email_test import send_email

def send_email():
    sender_email = "unanimousinfirmer111@gmail.com"
    receiver_email = "keerthanmgowda2@gmail.com"
    app_password = "zvqpqfwfdqfmzybe"

    subject = "RCB vs CSK Tickets LIVE"
    body = "Tickets are live. Open the site immediately. \n https://shop.royalchallengers.com/ticket" 
    

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)

        print("Email sent successfully")

    except Exception as e:
        print("Email failed:", e)