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
    subject = "RCB Tickets LIVE"
    body = f"Tickets are LIVE. Book immediately:\n{URL}"

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

    page = driver.page_source.lower()

    # STEP 1: Block false states
    if any(x in page for x in ["coming soon", "not available", "sold out"]):
        print("Tickets not available yet")
        return False

    # STEP 2: Look for real booking buttons
    buttons = driver.find_elements(By.TAG_NAME, "button")
    links = driver.find_elements(By.TAG_NAME, "a")

    # Strong signals (ONLY these trigger)
    trigger_words = ["buy now", "book now", "get tickets"]

    for btn in buttons:
        text = btn.text.lower().strip()
        if text in trigger_words:
            print("BOOKING BUTTON FOUND:", btn.text)
            return True

    for link in links:
        text = link.text.lower().strip()
        if any(word in text for word in ["buy", "book", "ticket"]):
            if len(text) < 40:  # avoid long irrelevant links
                print("BOOKABLE LINK FOUND:", link.text)
                return True

    print("No booking options yet")
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