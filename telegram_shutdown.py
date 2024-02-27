#!/usr/bin/python3
from telegram_notifications import TelegramNotifier
from dotenv import load_dotenv
from datetime import datetime

if __name__ == '__main__':
    load_dotenv()
    notifier = TelegramNotifier.default()

    message_arguments = {
        'date': datetime.now().strftime("%H:%M:%S - %d.%m.%Y")
    }

    message = """
🍓 <b>Raspberry PI is shutting down!</b> 

{date}""".format(**message_arguments)

    print("Sending a telegram SHUTDOWN notification...")
    notifier.send_message(message)
    print("Successfully sent a telegram SHUTDOWN notification")
