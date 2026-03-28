from datetime import datetime
import random

email_events = []

def send_email(to_email, subject, body):

    opened = random.choice([True, False])
    replied = opened and random.choice([True, False])

    event = {
        "email": to_email,
        "opened": opened,
        "replied": replied,
        "time": datetime.now().strftime("%H:%M:%S")
    }

    email_events.append(event)

    return event


def get_email_events():
    return email_events[-10:]