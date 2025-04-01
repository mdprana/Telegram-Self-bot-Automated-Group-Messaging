# Telegram Self-Bot for Automated Messaging

<div align="center">

![Telegram Logo](https://telegram.org/img/t_logo.svg)

*A Python script to automate message sending in Telegram groups at specified intervals*

⚠️ **USE AT YOUR OWN RISK: This tool violates Telegram's Terms of Service** ⚠️

</div>

## ⚠️ Disclaimer

This tool is created for educational purposes only. Using self-bots (automating a regular user account) violates Telegram's Terms of Service and may result in your account being limited or permanently banned. Key violations include:

- Automated usage of personal accounts
- Message flooding and spam
- Non-human behavior patterns

**The developers of this tool take no responsibility for any consequences resulting from its use. Proceed at your own risk.**

## 📋 Table of Contents

- [Telegram Self-Bot for Automated Messaging](#telegram-self-bot-for-automated-messaging)
  - [⚠️ Disclaimer](#️-disclaimer)
  - [📋 Table of Contents](#-table-of-contents)
  - [🔍 Overview](#-overview)
  - [✨ Features](#-features)
  - [📦 Requirements](#-requirements)
  - [💻 Installation](#-installation)
  - [🔧 Setup Guide](#-setup-guide)
  - [🚀 Usage](#-usage)
  - [⚙️ Configuration](#️-configuration)
  - [🔍 Finding Group IDs](#-finding-group-ids)
  - [🛡️ Minimizing Ban Risk](#️-minimizing-ban-risk)
  - [❓ Frequently Asked Questions](#-frequently-asked-questions)

## 🔍 Overview

This self-bot allows you to automatically send messages to Telegram groups at randomized intervals. It uses your personal Telegram account to send messages, making it appear as if you're sending them manually.

## ✨ Features

- 🕒 Customizable time intervals between messages
- 📝 Multiple message templates with randomized selection
- 🌐 Support for multiple groups simultaneously
- ⏰ Active hours setting to control when messages are sent
- 📊 Logging of all activities for monitoring
- 📋 Simple setup wizard for easy configuration

## 📦 Requirements

- Python 3.6 or higher
- Telethon library
- Telegram API credentials
- Active Telegram account

## 💻 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mdprana/Telegram-Self-bot-Automated-Group-Messaging.git
   cd Telegram-Self-bot-Automated-Group-Messaging
   ```

2. **Create a virtual environment (recommended):**
   
   On Windows:
   ```bash
   python -m venv .env
   .env\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   python3 -m venv .env
   source .env/bin/activate
   ```
   
   You'll see `(.env)` appear at the beginning of your terminal prompt, indicating the virtual environment is active.

3. **Install required dependencies:**
   ```bash
   pip install telethon
   ```
   
   When you're done using the bot, you can deactivate the virtual environment:
   ```bash
   deactivate
   ```

3. **Obtain Telegram API credentials:**
   - Visit [my.telegram.org/auth](https://my.telegram.org/auth)
   - Log in with your phone number
   - Go to "API development tools"
   - Create a new application (any name will do)
   - Note down your **API ID** and **API Hash**

## 🔧 Setup Guide

1. **Open `main.py` and replace the placeholder credentials:**
   ```python
   API_ID = 123456  # Replace with your API ID
   API_HASH = 'your_api_hash_here'  # Replace with your API hash
   PHONE_NUMBER = '+1234567890'  # Replace with your phone number
   ```

2. **Run the script:**
   ```bash
   python main.py
   ```

3. **Follow the interactive setup wizard:**
   - You'll be asked to authenticate with Telegram (first time only)
   - Enter the authentication code sent to your Telegram
   - Complete the setup by providing group IDs and message templates

## 🚀 Usage

After initial setup, the script will:

1. Connect to Telegram using your account
2. Find the specified groups by their IDs
3. Send random messages from your template list at the defined intervals
4. Log all activities to the console

To stop the script, press `Ctrl+C` in the terminal.

## ⚙️ Configuration

The configuration is stored in `config.json` and includes:

- `groups`: List of group IDs where messages will be sent
- `messages`: List of message templates (one will be randomly selected)
- `interval_min`: Minimum wait time between messages (in seconds)
- `interval_max`: Maximum wait time between messages (in seconds)
- `active_hours`: Time range when the bot is allowed to send messages

You can edit this file directly or rerun the setup wizard.

## 🔍 Finding Group IDs

A separate utility script is included to help you find group IDs:

1. Run the Group ID Finder:
   ```bash
   python group-id-finder.py
   ```

2. The script will list all your groups with their IDs:
   ```
   === GROUPS ===
   1. My Group Name
      ID: 1234567890
      Type: Supergroup
   ```

3. Use these numeric IDs when setting up the self-bot.

## 🛡️ Minimizing Ban Risk

To reduce the risk of account limitations:

- Set longer intervals between messages (30+ minutes recommended)
- Use diverse message templates that don't look automated
- Limit the number of groups you send to
- Only send content that's welcome in those groups
- Consider using Telegram's official Bot API instead for long-term automation

## ❓ Frequently Asked Questions

**Q: Is this against Telegram's Terms of Service?**  
A: Yes, automating a personal account violates Telegram's ToS.

**Q: What happens if I get caught?**  
A: Your account could be temporarily limited or permanently banned.

**Q: Can I send media files?**  
A: The current version only supports text messages. Media support may be added in future versions.

**Q: How do I make multi-line messages?**  
A: Use `\n` where you want line breaks. For example: `Hello!\n\nThis is a new paragraph.`

**Q: What's the safest interval between messages?**  
A: 30-60 minutes is generally safer than shorter intervals.

---

<div align="center">

📱 **Use Responsibly** 📱

*This project is not affiliated with or endorsed by Telegram*

</div>