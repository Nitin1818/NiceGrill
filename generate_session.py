from telethon.sync import TelegramClient
from telethon.sessions import StringSession


API_ID = int(input("Enter your API ID:"))
API_HASH = input("Enter your API HASH:")

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    string = client.session.save()
    print("Save this string session somewhere secure and use it any time. Do not share it")
    print(string)