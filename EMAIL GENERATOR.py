import json
import os
import re
import smtplib
import time
from datetime import datetime

from dotenv import load_dotenv
from mistralai import Mistral, UserMessage

load_dotenv()


flight_log = []
call_unique = []
number = []
api_key = os.getenv("api_key")
email = os.getenv("email")
password = os.getenv("password")


def get_daily_filename():

    today = datetime.now().strftime("%Y-%m-%d")
    return f"flightlog_{today}.json"


def load_daily_log():
    """Load today's log file if it exists."""
    global flight_log

    FILENAME = get_daily_filename()

    try:
        with open(FILENAME, "r") as f:
            flight_log = json.load(f)
    except:
        flight_log = []  # new day → fresh list


def save_daily_log():
    """Save today's updated flight log."""
    FILENAME = get_daily_filename()

    with open(FILENAME, "w") as f:
        json.dump(flight_log, f)


def list_of_flights():

    global flight_log, call_unique
    number_of_flights = []

    for flights in flight_log:
        if flights["callsign"] not in call_unique:
            call_unique.append(flights["callsign"])

    number_of_flights = len(call_unique)
    return number_of_flights


def email_maker():

    model = "mistral-large-latest"

    load_daily_log()
    number = list_of_flights()

    client = Mistral(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": f"""Write a professional but friendly email to [AIRPORT] about flight noise and how it affects my daily life.

            Details:
            - I recorded {number} flights over my house today
            - The recorded flights are due to [ADD YOUR AIRPORT] superhighway
            - Address: YOUR ADDRESS HERE
            - Name: YOUR NAME

            Requirements:
            - Keep it concise (150-200 words)
            - Start with a variation of "Dear [AIRPORT] Team,"
            - Avoid parralel phrasings like 'it's more than just an inconvenience, it's a way of...'
            - Use natural, conversational language (avoid corporate jargon)
            - Be polite but assertive
            - Mention in your own words 'I'll continue documenting daily flight counts'
            - Don't use em dashes (—) or overly formal phrases
            - Vary the wording each time - don't repeat phrases from previous emails
            - Make the subject a variation of 'Concerns About Flight Path [ADDRESS]'
            - Mention that you are not trying to do anything illegal or spammy, but you wish to share how my life is affected by how the airport is ran.

            Format:
            Subject: [create a brief subject line]

            [email body]

            Output ONLY the email with no additional commentary.""",
        },
    ]

    chat_response = client.chat.complete(
        model=model,
        messages=messages,
    )

    mistral_mail = chat_response.choices[0].message.content

    return mistral_mail


def email_sender(message, subject):

    # subject = mail_uncleaned[13:57:1]

    # Connect and authenticate
    smtp_object = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_object.starttls()
    smtp_object.login(email, password)

    # Send email
    from_address = email
    to_address = "[RECIPIENT EMAIL, PROBABLY AIRPORT]"

    msg = f"Subject: {subject}\n\n{message}"

    smtp_object.sendmail(from_address, to_address, msg.encode("utf-8"))
    smtp_object.quit()


def clean_email(email_text):

    # Remove markdown bold formatting
    email_text = email_text.replace("**", "")

    # Remove dashes
    email_text = email_text.replace("—", "; ")
    email_text = email_text.replace("–", ",")

    # Remove subject

    subject_match = re.search(
        r"Subject:\s*(.*?)(?=\n)", email_text, flags=re.IGNORECASE
    )
    subject_to_send = subject_match.group(1).strip() if subject_match else "No Subject"

    email_text = re.sub(
        r"^.*?(?=Dear)", "", email_text, flags=re.IGNORECASE | re.DOTALL
    )

    # Replace \n with actual newlines

    email_text = email_text.strip()

    return email_text, subject_to_send


# RUNNING SCRIPT

load_daily_log()
save_daily_log()
number = list_of_flights()
mail_uncleaned = email_maker()
cleaned_email, subject = clean_email(mail_uncleaned)
print(cleaned_email)
email_sender(cleaned_email, subject)
