import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import datetime

# ================= CONFIG =================
URL = "https://shop.royalchallengers.com/ticket"

SENDER_EMAIL = "unanimousinfirmer111@gmail.com"
RECEIVER_EMAIL = "keerthanmgowda2@gmail.com"
APP_PASSWORD = "zvqpqfwfdqfmzybe"
# ==========================================


def send_email():
    subject = "RCB vs CSK Tickets LIVE"
    body = f"Tickets are live:\n{URL}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("TICKET EMAIL SENT")


def send_no_ticket_email():
    subject = "No Tickets Update"
    body = "No tickets found in the last 12 hours."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("NO-TICKET EMAIL SENT")


def is_heartbeat_run():
    now = datetime.datetime.utcnow()
    return now.hour % 12 == 0 and now.minute < 5


def check_tickets(driver):
    driver.get(URL)
    time.sleep(5)

    print("Checking page...")

    buttons = driver.find_elements(By.TAG_NAME, "button")
    links = driver.find_elements(By.TAG_NAME, "a")

    for btn in buttons:
        text = btn.text.lower().strip()
        if text in ["buy now", "book now", "get tickets"]:
            print("REAL BUTTON FOUND:", btn.text)
            return True

    for link in links:
        text = link.text.lower().strip()
        if "csk" in text and ("buy" in text or "ticket" in text):
            print("MATCH FOUND:", link.text)
            return True

    return False


def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    found = check_tickets(driver)

    if found:
        send_email()
    elif is_heartbeat_run():
        send_no_ticket_email()

    driver.quit()


if __name__ == "__main__":
    main()