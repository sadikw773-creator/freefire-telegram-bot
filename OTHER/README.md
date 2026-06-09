# FREE FIRE TCP BOT - EMOTE

A sophisticated TCP bot for Free Fire that enables automated emotes, chat interactions, and squad management through direct server communication.

## ⚠️ Disclaimer

This project is for educational and research purposes only. Use at your own risk. The authors are not responsible for any consequences that may arise from the use of this software.

## 🚀 Features

- **Automated Emote System**: Trigger emotes automatically for yourself and squad members
- **Chat Bot Functionality**: Respond to commands and interact with players
- **TCP Connection Management**: Direct server communication with encryption
- **Squad Management**: Join/leave squads, handle invitations
- **Real-time Message Processing**: Process and respond to live game messages
- **Protocol Buffer Support**: Full protobuf integration for Free Fire's communication protocol

## 🛠️ Technical Features

- AES encryption/decryption for secure communication
- Protocol Buffer message serialization/deserialization
- TCP socket management with automatic reconnection
- Asynchronous I/O for high-performance message handling
- User authentication through Garena's OAuth system

## 📋 Requirements

- Python 3.9+ (recommended: 3.11 or 3.12)
- Free Fire account credentials
- All dependencies listed in `requirements.txt`

## 🖥️ Running Locally (Local Computer Setup)

**🇧🇩 বাংলায় সম্পূর্ণ গাইড:** [`LOCAL_SETUP_GUIDE_BANGLA.md`](LOCAL_SETUP_GUIDE_BANGLA.md)

**📋 Required Files Checklist:** [`REQUIRED_FILES_LIST.txt`](REQUIRED_FILES_LIST.txt)

For detailed Bengali instructions on running this bot on your local computer, including:
- Complete file list needed
- Step-by-step installation guide
- Troubleshooting tips
- System requirements

Please see the comprehensive guide above.

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/free-fire-tcp-bot-emote.git
cd free-fire-tcp-bot-emote
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Generate Protocol Buffer files:**
Make sure the `generated_proto/` directory contains the compiled Python protobuf files from the `.proto` definitions in the `proto/` directory.

## 🔧 Configuration

### 🔐 Method 1: সরাসরি Code-এ (Easiest - Simplest!)

**সবচেয়ে সহজ পদ্ধতি! `.env` file এর দরকার নেই।**

1. **Open `main.py` (around line 56-57)**

2. **Add your credentials:**
   ```python
   HARDCODED_BOT_UID = "your_bot_uid"
   HARDCODED_BOT_PASSWORD = "your_encrypted_password"
   ```

3. **Save and run!**
   ```bash
   python main.py
   ```

📘 **Detailed Guide (Bengali):** See [`CREDENTIALS_SETUP_BANGLA.md`](CREDENTIALS_SETUP_BANGLA.md)

⚠️ **Warning:** Remove credentials before pushing to GitHub!

---

### 🔐 Method 2: Using .env File (Recommended - More Secure!)

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and add your credentials:**
   ```env
   MAIN_BOT_UID=your_bot_uid
   MAIN_BOT_PASSWORD=your_encrypted_password
   FF_API_TOKEN=your_api_token  # Optional, for @info command
   ```

3. **Save and run!**

📘 **Detailed Guide (Bengali):** See [`ENV_SETUP_GUIDE_BANGLA.md`](ENV_SETUP_GUIDE_BANGLA.md)

### Step 2: Run the Bot

```bash
python main.py
```

## 🎮 Commands

The bot responds to various commands in the game chat:

### Basic Commands
- `/start` - Activate emote functionality and show available commands
- `/join <teamcode>` - Join a squad using the provided code
- `leave` - Leave the current squad

### Special Commands
- `/5` - Accept squad invitations automatically
- `/s` - Quick squad functionality

### Quick Emote Shortcuts 🎭 **NEW!**
Instant emotes to pre-configured players (no UID needed):
- `/m18` - M18 emote (909035007)
- `/p` - P emote (909000010)
- `/c` - C emote (909000014)
- `/gf` - GF emote (909000128)
- `/g` - G emote (909000143)
- `/m10` - M10 emote (909000081)
- `/flag` - Flag emote (909000034)
- `/car` - Car emote (909000039)
- `/bike` - Bike emote (909000074)
- `/par` - Par emote (909038009)
- `/fam` - Fam emote (909000145)
- `/mp4` - MP4 emote (909000075)
- `/xm8` - XM8 emote (909000085)
- `/hart` - Heart emote (909000045)

### Advanced Emote Commands 🎮
- `/ak` - Quick emote with default UIDs and emote ID
- `@a <uid> <emote_id> [region]` - Send emote to a specific player with region support
  - Example: `@a 123456789 909000001 BD` (sends emote to player in BD region)
  - Regions: IND, BD, or default
- `@emote <uid1> [uid2] [uid3] ... <emote_id> [region]` - Send emotes to multiple players
  - Example: `@emote 123456789 987654321 909000001 IND` (sends emote to 2 players)
  - Supports up to 5 UIDs simultaneously

### Player Information Commands 📊 **NEW!**
- `@info <uid>` - Get detailed player information (name, level, likes, guild, etc.)
  - Example: `@info 123456789`
  - Requires FF_API_TOKEN environment variable

### Player Search & Like Commands 💖
- `/search <player_uid> [region]` - Search for a player and view their profile
- `/like <player_uid> [region]` - Send likes to the specified player from all configured bot accounts
- `/likecount <player_uid> [region]` - Check how many likes a player has

**Region Support:**
- Default region: **BD** (Bangladesh Server - optimized for BD/India region)
- Supported regions: BD, IND, PK, BR, US, SG, ID, TH, VN, MY, and more
- If no region specified, BD server is used automatically

### Interactive Responses
The bot automatically responds to greetings like "hi", "hello", "fen", "salam" with a friendly message.

## 🔐 Environment Variables

The bot uses environment variables for secure credential management. You can set them using:

**Option 1: .env File (Recommended)**
```env
MAIN_BOT_UID=your_bot_uid
MAIN_BOT_PASSWORD=your_encrypted_password
FF_API_TOKEN=your_api_token  # Optional
DEFAULT_REGION=BD            # Optional, default region
WEB_PORT=5000               # Optional, web dashboard port
```

**Option 2: System Environment Variables**
- `MAIN_BOT_UID` - Main bot's Free Fire UID (Required)
- `MAIN_BOT_PASSWORD` - Main bot's encrypted password (Required)
- `FF_API_TOKEN` - Free Fire API token for player information features (@info command) (Optional)
- `DEFAULT_REGION` - Default region if not specified in commands (Optional, default: BD)
- `WEB_PORT` - Port for web dashboard (Optional, default: 5000)

## ⚡ Performance & Optimization

**🐌 Login slow হচ্ছে?** → [`PERFORMANCE_OPTIMIZATION_BANGLA.md`](PERFORMANCE_OPTIMIZATION_BANGLA.md) দেখুন

The bot makes 3 network requests during login (OAuth → MajorLogin → GetLoginData). Login speed depends on:
- Your internet connection quality
- Free Fire server response time  
- Network latency to servers

**Typical login times:**
- Fast network (50+ Mbps): 3-7 seconds
- Good network (10-50 Mbps): 5-10 seconds
- Slow network (<10 Mbps): 10-30 seconds

See the optimization guide for tips to improve performance.

🎥 **Watch Demo Video:** [Watch](https://youtu.be/LlrSCil3O9k)
