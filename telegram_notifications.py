#!/usr/bin/python3
from __future__ import annotations
from dotenv import load_dotenv
import requests, os, json

class TelegramError(RuntimeError):
    pass

class TelegramNotifier:
    token: str
    chat_id: int
    __url: str

    def default() -> TelegramNotifier:
        load_dotenv()
        token = os.getenv("TELEGRAM_API_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        return TelegramNotifier(token, chat_id)

    def __init__(self, token: str, chat_id: int) -> None:
        self.token = token
        self.chat_id = chat_id
        self.__url = f"https://api.telegram.org/bot{token}"
        
        # Check, if token is valid
        response = requests.get(f"{self.__url}/getMe")
        if (response.status_code == 401):
            raise ValueError(f"Provided API token is not valid: {token}")

    def send_message(self, text: str) -> None:
        request_body = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        request_headers = {
            "Content-Type": "application/json"
        }
        request_url = f"{self.__url}/sendMessage"

        response = requests.post(request_url, json=request_body, headers=request_headers)
        if (not response.ok):
            raise TelegramError(f"Telegram API request has failed with status {response.status_code}: '/sendMessage'", response.content)

if __name__ == "__main__":
    load_dotenv()
    telegram_notifier = TelegramNotifier.default()
    telegram_notifier.send_message("Foo.")
