#!/usr/bin/python3
from telegram_notifications import TelegramNotifier
from datetime import datetime
from dotenv import load_dotenv
import socket, requests, os

def get_local_ip() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 1))
    return sock.getsockname()[0]

def get_global_ip() -> str:
    ipv4_url = "https://api.ipify.org"
    ipv6_url = "https://api6.ipify.org"

    response = requests.get(ipv6_url)
    if (response.ok):
        return response.text
    response = requests.get(ipv4_url)
    if (response.ok):
        return response.text
    
    return None

class Service:
    id: str
    name: str

    def __init__(self, id: str, name: str = id) -> None:
        self.id = id
        self.name = name
        pass
    
    @property
    def is_active(self) -> bool:
        return os.system(f"systemctl is-active --quiet {self.id}") == 0
    
    @property
    def is_enabled(self) -> bool:
        return os.system(f"systemctl is-enabled --quiet {self.id}") == 0

    @property
    def status(self) -> str:
        if (not self.is_enabled):
            return "disabled"
        return "active" if self.is_active else "inactive"

def list_service_statuses(services: list[Service], format = "  {service}: <b>{status}</b>\n") -> str:
    result = ""
    for service in services:
        result += format.format(service = service.name, status = service.status)
    return result

if __name__ == '__main__':
    load_dotenv()
    notifier = TelegramNotifier.default()

    watched_services = [
        Service("minecraft-server.service", "Minecraft server"),
        Service("sshd.service", "SSH")
    ]

    message_arguments = {
        'hostname': socket.gethostname(),
        'ip_local': get_local_ip(),
        'ip_global': get_global_ip(),
        'services': list_service_statuses(watched_services),
        'date': datetime.now().strftime("%H:%M:%S - %d.%m.%Y")
    }

    message = """
🍓 <b>Raspberry PI is online</b>

Hostname: <code>{hostname}</code>
Local IP: <code>{ip_local}</code>
Global IP: <code>{ip_global}</code>

<b>Services:</b>
{services}
{date}""".format(**message_arguments)

    print("Sending a telegram BOOT notification...")
    notifier.send_message(message)
    print("Successfully sent a telegram BOOT notification")
