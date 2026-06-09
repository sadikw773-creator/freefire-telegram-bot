# Free Fire TCP Bot - Emote & Like System

## ⚠️ OB51 Compatibility Status

**Current Status**: 🟡 **PARTIAL COMPATIBILITY - AUTHENTICATION MAY FAIL**

**What's Been Updated (October 29, 2025):**
- ✅ ReleaseVersion changed from "OB50" to "OB51" (main.py line 65)

**What's Still Needed for Full OB51 Support:**
- ❌ `client_version` (currently "1.114.1" from OB50 - line 130 in main.py)
- ❌ `client_version_code` (currently "2019118695" from OB50 - line 171 in main.py)  
- ❌ `client_using_version` hash (currently OB50 hash - line 155 in main.py)

**Impact**: 
- ✅ **Web Dashboard** (port 5000): Player search, like sending - **WORKS NORMALLY**
- ⚠️ **Console TCP Bot** (main.py): Authentication **MAY FAIL** due to server rejecting outdated client metadata

**How to Complete OB51 Update (For Advanced Users):**
1. Download official OB51 APK (v66.51.0) from https://ff.garena.com/
2. Decompile APK using JADX: `jadx free-fire-ob51.apk -d ob51_source/`
3. Search for MajorLogin payload to find correct client_version and client_version_code
4. Update these values in main.py (lines 130, 171, 155)
5. Test authentication against live OB51 servers

## Overview
This project is a Python-based TCP bot for Free Fire, designed to automate in-game actions such as sending emotes, managing squads, interacting via chat, searching for players, and sending likes. It communicates directly with Free Fire game servers using TCP sockets and encrypted Protocol Buffers. The project also features a Flask-based web dashboard for a user-friendly interface. It is currently being updated for Free Fire OB51 (v66.51.0), with partial compatibility achieved.

## User Preferences
None set yet. Add any coding style preferences or workflow preferences here.

## System Architecture

### Core Components
- **main.py**: Orchestrates bot logic, authentication, connection, chat, emote, and like/search functionalities.
- **network_utils.py**: Handles AES encryption/decryption and Protocol Buffer encoding/decoding.
- **like_utils.py**: Manages player search, like sending, and JWT authentication.
- **player_utils.py**: Provides player information retrieval and API functions.
- **generated_proto/**: Compiled Python Protocol Buffer files.
- **like_proto/** and **proto/**: Source Protocol Buffer definition files.
- **Flask Web Dashboard**: Provides a modern, responsive UI with real-time statistics, player search, like sending, and multi-region support.

### Technology Stack
- **Python 3.11**: Primary programming language.
- **asyncio**: For asynchronous I/O operations.
- **aiohttp** & **httpx**: Asynchronous HTTP clients for API requests.
- **pycryptodome**: For AES encryption in secure server communication.
- **protobuf**: For serializing game messages.
- **Flask**: For the web dashboard.
- **Free Fire OB51**: Compatibility target for the bot.

### Key Features
- **Authentication**: OAuth-based authentication via Garena.
- **TCP Connection Management**: Direct server communication with auto-reconnection.
- **Encrypted Communication**: AES encryption/decryption for all messages.
- **Advanced Help System**: In-game commands like `/help`, `/status`, `/about`.
- **Smart Like System**: Randomly selects 100 out of 254 bot accounts for each like request.
- **Background Processing**: `/like` and `/5` commands run concurrently.
- **Enhanced Error Handling**: Provides usage examples for commands.
- **Chat Bot**: Responds to in-game chat commands.
- **Emote System**: Automated and advanced emote triggering with region support to specific players or multiple players.
- **Squad Management**: Join/leave squads and handle invitations.
- **Player Information**: Retrieve detailed player profiles (`@info <uid>`).
- **Player Search & Like**: Search players by UID (`/search`) and send bulk likes (`/like`) with multi-region support.
- **Multi-Region Support**: Full support for various regions including IND, BD, SG, BR.

### Configuration
- **Main Bot Credentials**: `MAIN_BOT_UID` and `MAIN_BOT_PASSWORD` loaded securely from environment variables.
- **Like Bot Accounts**: Configured in `like_bot_accounts.py` for sending multiple likes.
- **Environment Variables**:
    - `MAIN_BOT_UID` (Required): Main bot's Free Fire UID.
    - `MAIN_BOT_PASSWORD` (Required): Main bot's encrypted password.
    - `FF_API_TOKEN` (Optional): Free Fire API token for detailed player information.

## External Dependencies
- **Free Fire Game Servers**: Direct TCP socket communication.
- **Garena's OAuth System**: For authentication.
- **Free Fire Public APIs**: For player data, search, and like functionalities.