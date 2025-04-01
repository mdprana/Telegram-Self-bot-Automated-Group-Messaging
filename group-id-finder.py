import asyncio
import logging
from telethon import TelegramClient

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram API credentials - REPLACE THESE WITH YOUR OWN
API_ID = 123456  # Replace with your API ID
API_HASH = 'your_api_hash_here'  # Replace with your API hash
PHONE_NUMBER = '+1234567890'  # Replace with your phone number

async def main():
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(PHONE_NUMBER)
    
    print("\n=== Telegram Group ID Finder ===\n")
    print("Fetching your dialogs (chats and groups)...")
    
    dialogs = await client.get_dialogs()
    
    # Create lists to organize chats by type
    groups = []
    channels = []
    private_chats = []
    
    for dialog in dialogs:
        entity = dialog.entity
        
        # Get the ID
        chat_id = getattr(entity, 'id', None)
        
        # Get the title or name
        if hasattr(entity, 'title'):
            name = entity.title
        elif hasattr(entity, 'first_name'):
            if hasattr(entity, 'last_name') and entity.last_name:
                name = f"{entity.first_name} {entity.last_name}"
            else:
                name = entity.first_name
        else:
            name = "Unknown"
        
        # Categorize based on attributes
        if hasattr(entity, 'megagroup') and entity.megagroup:
            groups.append((name, chat_id, 'Supergroup'))
        elif hasattr(entity, 'gigagroup') and entity.gigagroup:
            groups.append((name, chat_id, 'Gigagroup'))
        elif hasattr(entity, 'broadcast') and entity.broadcast:
            channels.append((name, chat_id, 'Channel'))
        elif hasattr(entity, 'participants_count'):
            groups.append((name, chat_id, 'Group'))
        else:
            private_chats.append((name, chat_id, 'Private'))
    
    # Print groups
    if groups:
        print("\n=== GROUPS ===")
        for idx, (name, chat_id, type_) in enumerate(groups, 1):
            print(f"{idx}. {name}")
            print(f"   Type: {type_}")
            print()
    
    # Print channels
    if channels:
        print("\n=== CHANNELS ===")
        for idx, (name, chat_id, type_) in enumerate(channels, 1):
            print(f"{idx}. {name}")
            print(f"   Type: {type_}")
            print()
    
    # Ask if they want to see private chats as well
    if private_chats:
        show_private = input("Do you want to see private chats as well? (y/n): ").lower() == 'y'
        if show_private:
            print("\n=== PRIVATE CHATS ===")
            for idx, (name, chat_id, type_) in enumerate(private_chats, 1):
                print(f"{idx}. {name}")
                print()
    
    print("\nTo use a group in the self-bot, enter its ID when prompted, prefixed with 'id:'")
    print("Example: id:-1001234567890")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())