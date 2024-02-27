# raspberry-notifications

This project includes scripts sending notifications on various
machine actions, such as bootup and shutdown.
Scripts are oriented for my Raspberry PI and send messages to
me via a Telegram bot.

## How to use

1. Clone this project using `git clone https://github.com/Avatcher/raspberry-notifications.git`
2. Move cloned project into `/opt/script/telegram-notification`
3. Define the next variables in root `.env` file:
```properties
# Telegram API token
TELEGRAM_API_TOKEN=

# ID of the chat to send notifications to.
# You can get chat id of your DMs using @getmyid_bot
TELEGRAM_CHAT_ID=
```
4. Run [`./service-units/update.sh`](./service-units/update.sh) with sudo rights
5. Done!

