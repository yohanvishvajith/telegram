
from telethon import TelegramClient, events
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch credentials from environment variables
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')  # Your Telegram phone number with country code

client = TelegramClient('session_name', API_ID, API_HASH)

async def dump_messages():
    print("Fetching recent messages...")
    async for message in client.iter_messages('me'):  # Fetching messages from 'me' (your personal chat)
        print(f'{message.sender_id}: {message.text}')

async def dump_contacts():
    print("Fetching contacts...")
    dialogs = await client.get_dialogs()  # Fetch all dialogs (including personal chats)
    for dialog in dialogs:
        if dialog.is_user:  # Check if the dialog is a personal chat
            print(f'Name: {dialog.name}, Username: {dialog.username if dialog.username else "No Username"}, ID: {dialog.id}')

async def dump_group_messages():
    print("Fetching messages from a group...")
    group_name = input("Enter the group name or username (e.g., 'group_name' or 'https://t.me/group_name'): ")
    
    try:
        async for message in client.iter_messages(group_name):
            print(f'{message.sender_id}: {message.text}')
    except Exception as e:
        print(f"Could not fetch messages from group: {e}")

async def dump_group_share_link():
    print("Fetching shareable group link...")
    group_name = input("Enter the group name or username (e.g., 'group_name' or 'https://t.me/group_name'): ")
    try:
        invite_link = await client.export_chat_invite_link(group_name)
        print(f"Invite Link: {invite_link}")
    except Exception as e:
        print(f"Could not fetch link: {e}")

async def dump_personal_info():
    print("Fetching personal information...")
    me = await client.get_me()  # Get personal info from your Telegram account
    print(f'Name: {me.first_name} {me.last_name}')
    print(f'Username: {me.username if me.username else "No Username"}')
    print(f'Phone number: {me.phone}')
    print(f'Bio: {me.bio if me.bio else "No Bio"}')

async def menu():
    await client.start(phone=PHONE_NUMBER)
    
    while True:
        print("\n--- Menu ---")
        print("1. Dump Messages")
        print("2. Dump Contacts")
        print("3. Dump Group Messages")
        print("4. Dump Group Share Link")
        print("5. Dump Personal Info")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            await dump_messages()
        elif choice == "2":
            await dump_contacts()
        elif choice == "3":
            await dump_group_messages()
        elif choice == "4":
            await dump_group_share_link()
        elif choice == "5":
            await dump_personal_info()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(menu())
