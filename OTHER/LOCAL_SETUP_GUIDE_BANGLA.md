# 🖥️ FREE FIRE BOT - LOCAL COMPUTER এ RUN করার সম্পূর্ণ গাইড

## 📋 যে ফাইলগুলো লাগবে

আপনার local computer-এ এই bot টি run করতে হলে নিচের সব ফাইল এবং ফোল্ডারগুলো লাগবে:

### ✅ প্রধান ফাইলসমূহ (Mandatory Files)

#### 1. **Python Code Files** (মূল কোড ফাইল)
- `main.py` - Console-based bot run করার জন্য main file
- `web_app.py` - Web dashboard (browser-এ দেখার জন্য)
- `network_utils.py` - Network connection handling
- `like_utils.py` - Player search এবং like functionality
- `player_utils.py` - Player information retrieval
- `emote_shortcuts.py` - Emote shortcut configuration
- `like_bot_accounts.py` - Like bot accounts এর list

#### 2. **Configuration Files** (কনফিগারেশন ফাইল)
- `requirements.txt` - সব Python packages এর list (updated and cleaned)
- `README.md` - Project documentation
- `replit.md` - Project information

#### 3. **Protocol Buffer Files** (জরুরী)
এই ফোল্ডার এবং এর ভেতরের সব ফাইল লাগবে:

**`generated_proto/` ফোল্ডার:**
- `__init__.py`
- `DEcwHisPErMsG_pb2.py`
- `MajoRLoGinrEq_pb2.py`
- `MajoRLoGinrEs_pb2.py`
- `PorTs_pb2.py`
- `sQ_pb2.py`

**`like_proto/` ফোল্ডার:**
- `__init__.py`
- `send_like_pb2.py`

**`proto/` ফোল্ডার:** (Optional - already compiled থাকলে)
- `DecodeWhisperMsg.proto`
- `GetLoginDataRes.proto`
- `MajorLoginReq.proto`
- `MajorLoginRes.proto`
- `recieved_chat.proto`
- এবং অন্যান্য `.proto` files

#### 4. **Web Dashboard Template**
**`templates/` ফোল্ডার:**
- `index.html` - Web interface

---

## 🔧 Installation Steps (ইনস্টলেশন প্রক্রিয়া)

### Step 1: Python Install করুন
- **প্রয়োজনীয় Python Version:** Python 3.9 অথবা তার উপরে (3.9, 3.10, 3.11, 3.12, 3.13)
- Download: https://www.python.org/downloads/

**Windows এ:**
- Python installer download করুন
- Install করার সময় **"Add Python to PATH"** অপশন চেক করুন

**Linux/Mac এ:**
```bash
sudo apt update
sudo apt install python3.9 python3-pip
```

### Step 2: সব ফাইল Download/Copy করুন
- এই project এর সব ফাইল এবং ফোল্ডার একটি ফোল্ডারে রাখুন
- উদাহরণ: `C:\Users\YourName\FreeFire-Bot\` অথবা `~/FreeFire-Bot/`

### Step 3: Dependencies Install করুন
Terminal/Command Prompt open করুন এবং bot এর ফোল্ডারে যান:

**Windows এ:**
```cmd
cd C:\Users\YourName\FreeFire-Bot
pip install -r requirements.txt
```

**Linux/Mac এ:**
```bash
cd ~/FreeFire-Bot/
pip3 install -r requirements.txt
```

### Step 4: Configuration Setup (গুরুত্বপূর্ণ!)

#### 🔐 Method 1: .env File ব্যবহার করুন (Recommended - সবচেয়ে সহজ!)

**`.env` file হলো সবচেয়ে secure এবং সহজ পদ্ধতি credentials রাখার জন্য!**

**Quick Setup:**
1. `.env.example` file কপি করে নাম পরিবর্তন করুন `.env`
   ```bash
   cp .env.example .env
   ```

2. `.env` file open করে আপনার credentials দিন:
   ```env
   MAIN_BOT_UID=আপনার_বট_UID
   MAIN_BOT_PASSWORD=আপনার_এনক্রিপ্টেড_পাসওয়ার্ড
   FF_API_TOKEN=আপনার_API_টোকেন (optional)
   ```

3. File save করুন এবং bot run করুন!

📘 **বিস্তারিত গাইড:** [`ENV_SETUP_GUIDE_BANGLA.md`](ENV_SETUP_GUIDE_BANGLA.md) দেখুন

---

#### 🔧 Method 2: Code-এ সরাসরি দিন (Alternative)

`main.py` ফাইল open করুন এবং line 480-481 এর কাছে খুঁজুন:

```python
user_credentials = ("YOUR_BOT_ID", "YOUR_PASSWORD")
```

এখানে `YOUR_BOT_ID` এবং `YOUR_PASSWORD` এর জায়গায় আপনার **Free Fire account credentials** দিন।

⚠️ **সতর্কতা:** এই method-এ credentials code-এ থাকবে, তাই GitHub-এ upload করার আগে remove করতে ভুলবেন না!

#### 4.2: Like Bot Accounts Setup (Optional)
`like_bot_accounts.py` ফাইলে আপনার multiple bot accounts যোগ করুন:

```python
LIKE_BOT_ACCOUNTS = [
    ("BOT_UID_1", "BOT_PASSWORD_1"),
    ("BOT_UID_2", "BOT_PASSWORD_2"),
    # আরও accounts যোগ করুন...
]
```

#### 4.3: API Token Setup (Optional - @info command এর জন্য)
Environment variable সেট করুন:

**Windows এ:**
```cmd
set FF_API_TOKEN=your_ff_api_token_here
```

**Linux/Mac এ:**
```bash
export FF_API_TOKEN=your_ff_api_token_here
```

---

## 🚀 Bot Run করার পদ্ধতি

### Method 1: Console Bot Run করুন (Terminal-based)
Terminal/Command Prompt এ:

```bash
python main.py
```

এটা console-এ bot চালু করবে এবং আপনি terminal-এ সব logs দেখতে পারবেন।

### Method 2: Web Dashboard Run করুন (Browser-based)
Terminal/Command Prompt এ:

```bash
python web_app.py
```

এরপর আপনার browser-এ যান: `http://localhost:5000`

এখানে আপনি:
- Bot control করতে পারবেন
- Player search করতে পারবেন
- Like পাঠাতে পারবেন
- Statistics দেখতে পারবেন

---

## 📁 ফোল্ডার Structure (সম্পূর্ণ)

```
FreeFire-Bot/
│
├── main.py                        # Main console bot
├── web_app.py                     # Web dashboard
├── network_utils.py               # Network utilities
├── like_utils.py                  # Like functionality
├── player_utils.py                # Player info utilities
├── emote_shortcuts.py             # Emote shortcuts
├── like_bot_accounts.py           # Like bot accounts config
├── requirements.txt               # Python dependencies (UPDATED + python-dotenv)
├── .env                           # আপনার credentials (secret! GitHub এ যাবে না)
├── .env.example                   # Example template
├── .gitignore                     # Git ignore rules
├── README.md                      # Documentation
├── replit.md                      # Project info
├── LOCAL_SETUP_GUIDE_BANGLA.md    # Local setup guide
├── ENV_SETUP_GUIDE_BANGLA.md      # .env file setup guide
├── REQUIRED_FILES_LIST.txt        # Required files checklist
│
├── generated_proto/               # Compiled protobuf files
│   ├── __init__.py
│   ├── DEcwHisPErMsG_pb2.py
│   ├── MajoRLoGinrEq_pb2.py
│   ├── MajoRLoGinrEs_pb2.py
│   ├── PorTs_pb2.py
│   └── sQ_pb2.py
│
├── like_proto/                    # Like protobuf files
│   ├── __init__.py
│   └── send_like_pb2.py
│
├── proto/                         # Original .proto definitions
│   ├── DecodeWhisperMsg.proto
│   ├── GetLoginDataRes.proto
│   ├── MajorLoginReq.proto
│   ├── MajorLoginRes.proto
│   └── recieved_chat.proto
│
└── templates/                     # Web dashboard templates
    └── index.html
```

---

## 🛠️ Troubleshooting (সমস্যা সমাধান)

### Problem 1: "Python not found" বা "pip not found"
**Solution:**
- Python সঠিকভাবে install হয়েছে কিনা চেক করুন
- PATH-এ Python add করা আছে কিনা verify করুন
- Terminal/CMD restart করুন

### Problem 2: Module Import Error
```
ModuleNotFoundError: No module named 'xxx'
```

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Problem 3: Protocol Buffer Error
**Solution:**
- `generated_proto/` ফোল্ডারের সব ফাইল আছে কিনা চেক করুন
- `__init__.py` files missing হলে empty file create করুন

### Problem 4: Web Dashboard খুলছে না
**Solution:**
- Port 5000 already use হচ্ছে কিনা চেক করুন
- Firewall block করছে কিনা দেখুন
- `http://127.0.0.1:5000` try করুন `localhost` এর বদলে

### Problem 5: Connection Error / Network Issue
**Solution:**
- Internet connection চেক করুন
- VPN use করলে বন্ধ করে দেখুন
- Antivirus/Firewall allow করা আছে কিনা চেক করুন

---

## ⚙️ System Requirements (সিস্টেম রিকোয়ারমেন্টস)

### Minimum Requirements:
- **OS:** Windows 7/8/10/11, Linux (Ubuntu 18.04+), macOS 10.14+
- **Python:** 3.9 বা তার উপরে
- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** 500MB free space
- **Internet:** Stable internet connection (broadband recommended)

### Recommended Requirements:
- **OS:** Windows 10/11, Ubuntu 20.04+, macOS 11+
- **Python:** 3.11 বা 3.12
- **RAM:** 4GB বা তার বেশি
- **Storage:** 1GB free space
- **Internet:** 5 Mbps+ stable connection

---

## 🔐 Security Tips (নিরাপত্তা টিপস)

1. **কখনও** আপনার bot credentials শেয়ার করবেন না
2. Public repository-তে push করার আগে credentials remove করুন
3. Strong passwords use করুন
4. API tokens secure রাখুন
5. অপরিচিত কারো সাথে bot files শেয়ার করবেন না

---

## 📞 Support & Help

যদি কোনো সমস্যা হয়:
1. Error message ভালো করে পড়ুন
2. Troubleshooting section দেখুন
3. Google-এ error search করুন
4. GitHub issues চেক করুন

---

## ⚠️ Disclaimer (গুরুত্বপূর্ণ সতর্কতা)

এই bot **শুধুমাত্র educational এবং research purposes** এর জন্য তৈরি করা হয়েছে।
- Use করার আগে Free Fire এর Terms of Service পড়ুন
- Bot use করলে account ban হতে পারে
- নিজ দায়িত্বে use করুন
- Developers কোনো সমস্যার জন্য দায়ী নয়

---

## ✅ Final Checklist (শেষ চেক করুন)

Run করার আগে নিশ্চিত করুন:
- [ ] Python 3.9+ installed আছে
- [ ] সব required files এবং folders আছে
- [ ] `pip install -r requirements.txt` successfully হয়েছে
- [ ] Bot credentials `main.py`-তে সেট করা আছে
- [ ] Internet connection active আছে
- [ ] Firewall/Antivirus allow করা আছে

এখন আপনি ready! 🎉

**Console Bot:** `python main.py`
**Web Dashboard:** `python web_app.py` (তারপর browser-এ `http://localhost:5000`)

---

**ডেভেলপমেন্ট টিম আপনার সাফল্য কামনা করছে!** 🚀
