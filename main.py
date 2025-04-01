import asyncio
import logging
import time
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import random
import json
import os

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram API credentials - REPLACE THESE WITH YOUR OWN
API_ID = 123456  # Replace with your API ID
API_HASH = 'your_api_hash_here'  # Replace with your API hash
PHONE_NUMBER = '+1234567890'  # Replace with your phone number

# Configuration
CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    'groups': [],  # List of group IDs to send messages to
    'messages': [  # List of messages to send (randomly selected)
        "Hello everyone! How are you doing today?",
        "Just checking in. Hope everyone is having a great day!",
        "Don't forget about our upcoming event!"
    ],
    'interval_min': 3600,  # Minimum interval between messages (in seconds) - 1 hour
    'interval_max': 7200,  # Maximum interval between messages (in seconds) - 2 hours
    'active_hours': {  # Hours when the bot is allowed to send messages (24-hour format)
        'start': 9,  # 9 AM
        'end': 21    # 9 PM
    }
}

class TelegramSelfBot:
    def __init__(self):
        self.client = None
        self.running = False
        self.config = self.load_config()
        self.group_entities = []

    def load_config(self):
        """Load configuration from file or create with defaults if it doesn't exist."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                logger.info("Configuration loaded successfully")
                return config
            except Exception as e:
                logger.error(f"Error loading configuration: {e}")
        
        # Create default config file if it doesn't exist
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        logger.info("Created default configuration file")
        return DEFAULT_CONFIG

    def save_config(self):
        """Save current configuration to file."""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)
        logger.info("Configuration saved")

    async def connect(self):
        """Connect to Telegram and authenticate."""
        self.client = TelegramClient('session_name', API_ID, API_HASH)
        await self.client.start(PHONE_NUMBER)
        logger.info("Connected to Telegram")

    async def get_dialogs(self):
        """Get all dialogs (chats and groups)."""
        try:
            # Try the simpler method first
            dialogs = await self.client.get_dialogs()
            return dialogs
        except Exception as e:
            logger.error(f"Error using get_dialogs(): {e}")
            
            # Fall back to the more complex method
            try:
                result = await self.client(GetDialogsRequest(
                    offset_date=None,
                    offset_id=0,
                    offset_peer=InputPeerEmpty(),
                    limit=200,
                    hash=0
                ))
                return result.dialogs
            except Exception as e2:
                logger.error(f"Error using GetDialogsRequest: {e2}")
                return []

    async def find_groups(self):
        """Find all the specified groups in the config."""
        self.group_entities = []
        
        # First, try to get all dialogs to print available groups for reference
        try:
            dialogs = await self.get_dialogs()
            logger.info("Available groups:")
            for dialog in dialogs:
                try:
                    chat = dialog.entity if hasattr(dialog, 'entity') else dialog
                    if hasattr(chat, 'title'):
                        chat_id = getattr(chat, 'id', 'Unknown')
                        logger.info(f"  - {chat.title} (ID: {chat_id})")
                except Exception as e:
                    pass
        except Exception as e:
            logger.error(f"Error listing available groups: {e}")
        
        # Attempt to directly resolve each ID
        for group_id in self.config['groups']:
            try:
                # Clean up the input - remove any non-numeric characters
                clean_id = ''.join(c for c in group_id if c.isdigit())
                if not clean_id:
                    logger.warning(f"Invalid group ID: {group_id}")
                    continue
                    
                # Convert to integer
                numeric_id = int(clean_id)
                
                # Try to get the entity directly
                entity = await self.client.get_entity(numeric_id)
                
                if entity:
                    self.group_entities.append(entity)
                    title = getattr(entity, 'title', f"Group {numeric_id}")
                    logger.info(f"Successfully added group: {title} (ID: {numeric_id})")
            except Exception as e:
                logger.error(f"Failed to resolve group ID {group_id}: {e}")
                
        if not self.group_entities:
            logger.warning("No groups found. Please check your configuration.")

    def is_active_hour(self):
        """Check if current time is within active hours."""
        current_hour = datetime.now().hour
        start_hour = self.config['active_hours']['start']
        end_hour = self.config['active_hours']['end']
        return start_hour <= current_hour < end_hour

    async def send_message_to_group(self, group):
        """Send a random message to a specific group."""
        if not self.is_active_hour():
            logger.info("Outside of active hours, skipping message")
            return
        
        message = random.choice(self.config['messages'])
        try:
            await self.client.send_message(group, message)
            group_title = getattr(group, 'title', 'Unknown Group')
            logger.info(f"Message sent to {group_title}: {message}")
        except Exception as e:
            group_title = getattr(group, 'title', 'Unknown Group')
            logger.error(f"Error sending message to {group_title}: {e}")

    async def message_scheduler(self):
        """Schedule and send messages at random intervals."""
        while self.running:
            for group in self.group_entities:
                await self.send_message_to_group(group)
            
            # Calculate next interval
            interval = random.randint(
                self.config['interval_min'], 
                self.config['interval_max']
            )
            
            logger.info(f"Next message will be sent in {interval//60} minutes")
            await asyncio.sleep(interval)

    async def start_bot(self):
        """Start the self-bot."""
        await self.connect()
        await self.find_groups()
        
        if not self.group_entities:
            logger.error("No valid groups found. Exiting.")
            return
        
        self.running = True
        logger.info("Bot started. Press Ctrl+C to stop.")
        await self.message_scheduler()

    async def stop_bot(self):
        """Stop the self-bot."""
        self.running = False
        if self.client:
            await self.client.disconnect()
        logger.info("Bot stopped")

    def setup_interactive(self):
        """Interactive setup to configure the bot."""
        print("=== Telegram Self-Bot Setup ===")
        
        # Get groups
        print("Enter group IDs separated by commas (just the numbers):")
        print("Example: 1554996935, 2406226933, 2193706526")
        groups = input("> ").split(',')
        self.config['groups'] = [g.strip() for g in groups if g.strip()]
        
        # Get messages
        print("Enter messages to send. For multi-line messages, type '\\n' where you want a line break.")
        print("Enter one message at a time, and press Enter with an empty line to finish:")
        messages = []
        while True:
            msg = input("> ")
            if not msg:
                break
            # Replace the literal \n with actual newline characters
            msg = msg.replace('\\n', '\n')
            messages.append(msg)
        
        if messages:
            self.config['messages'] = messages
        
        # Get intervals
        try:
            min_interval = int(input("Minimum interval between messages (in minutes): "))
            max_interval = int(input("Maximum interval between messages (in minutes): "))
            if min_interval > 0 and max_interval >= min_interval:
                self.config['interval_min'] = min_interval * 60
                self.config['interval_max'] = max_interval * 60
        except ValueError:
            print("Invalid input. Using default intervals.")
        
        # Get active hours
        try:
            start_hour = int(input("Start hour (0-23): "))
            end_hour = int(input("End hour (0-23): "))
            if 0 <= start_hour < 24 and 0 <= end_hour <= 24:
                self.config['active_hours']['start'] = start_hour
                self.config['active_hours']['end'] = end_hour
        except ValueError:
            print("Invalid input. Using default active hours.")
        
        self.save_config()
        print("Configuration saved!")

async def main():
    bot = TelegramSelfBot()
    
    if not bot.config['groups'] or input("Run setup wizard? (y/n): ").lower() == 'y':
        bot.setup_interactive()
    
    try:
        await bot.start_bot()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        await bot.stop_bot()

if __name__ == "__main__":
    asyncio.run(main())