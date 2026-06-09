# 🔐 .ENV FILE SETUP GUIDE (Bengali)

## .env File কি এবং কেন লাগবে?

`.env` file হলো একটি configuration file যেখানে আপনার **sensitive information** (যেমন passwords, API keys) secure ভাবে রাখা হয়। এটা ব্যবহার করলে:

✅ **সুবিধা:**
- আপনার credentials code-এর বাইরে থাকে
- সহজে change করা যায়
- GitHub-এ upload হওয়ার ভয় নেই (`.gitignore`-এ আছে)
- একাধিক environment-এ ভিন্ন credentials use করা যায়

---

## 📋 Step-by-Step Setup (ধাপে ধাপে সেটআপ)

### Step 1: `.env.example` File কপি করুন

আপনার bot folder-এ একটি `.env.example` file দেওয়া আছে। এটাকে copy করে নাম পরিবর্তন করুন:

**Windows এ:**
```cmd
copy .env.example .env
```

**Linux/Mac এ:**
```bash
cp .env.example .env
```

অথবা manually:
1. `.env.example` file open করুন
2. "Save As" করে নাম দিন `.env`
3. Same folder-এ save করুন

---

### Step 2: `.env` File Edit করুন

`.env` file একটি text editor দিয়ে open করুন (Notepad, VS Code, Sublime, etc.)

আপনি দেখবেন:

```env
# Main Bot Credentials
MAIN_BOT_UID=YOUR_BOT_UID_HERE
MAIN_BOT_PASSWORD=YOUR_ENCRYPTED_PASSWORD_HERE

# API Token (Optional)
FF_API_TOKEN=

# Settings
DEFAULT_REGION=BD
WEB_PORT=5000
```

---

### Step 3: আপনার তথ্য দিন

#### 3.1 Main Bot Credentials (Required - অবশ্যই লাগবে)

```env
MAIN_BOT_UID=4245749321
MAIN_BOT_PASSWORD=71496B76FB9E4BA2C14F80D7A75A5DD25F75793F267E4C21B73D662881404ED1
```

**কিভাবে পাবেন:**
- `MAIN_BOT_UID` = আপনার Free Fire account এর UID
- `MAIN_BOT_PASSWORD` = Encrypted password (আপনার FF account password, encrypted format-এ)

⚠️ **Important:** Password টি encrypted format-এ লাগবে (raw password নয়)

---

#### 3.2 API Token (Optional - ঐচ্ছিক)

```env
FF_API_TOKEN=your_api_token_here_1234567890
```

এটা শুধু `@info` command এর জন্য লাগে। যদি player এর detailed information দেখতে চান, তাহলে এটা add করুন।

**না থাকলে কি হবে:** শুধু `@info` command কাজ করবে না, বাকি সব কাজ করবে।

---

#### 3.3 Additional Settings (Optional)

```env
DEFAULT_REGION=BD
WEB_PORT=5000
```

- `DEFAULT_REGION` = যদি কোনো command-এ region উল্লেখ না থাকে, কোন region use করবে (Default: BD)
- `WEB_PORT` = Web dashboard কোন port-এ run করবে (Default: 5000)

---

### Step 4: File Save করুন

✅ `.env` file save করে close করুন

⚠️ **নিশ্চিত করুন:**
- File name ঠিক আছে: `.env` (`.env.txt` নয়!)
- Bot folder-এর main directory-তে আছে (যেখানে `main.py` আছে)

---

## 🚀 Bot Run করুন

এখন আপনি normal ভাবে bot run করতে পারবেন:

```bash
# Console bot
python main.py

# Web dashboard
python web_app.py
```

Bot automatically `.env` file থেকে credentials load করবে! 🎉

---

## 📂 File Structure (সঠিক structure)

```
FreeFire-Bot/
├── .env                    ← আপনার actual credentials (secret!)
├── .env.example            ← Example template
├── .gitignore              ← .env ignore করে (safety!)
├── main.py
├── web_app.py
├── requirements.txt
└── ... (other files)
```

---

## ✅ Verify করুন (চেক করুন)

Bot run করার পর terminal-এ দেখুন কোনো error আসছে কিনা:

**ভালো Output (সফল):**
```
[SUCCESS] Environment loaded from .env file
[INFO] Bot UID: 4245749321
[INFO] Starting bot...
```

**খারাপ Output (সমস্যা):**
```
[WARNING] MAIN_BOT_UID not set
[ERROR] Failed to authenticate
```

---

## 🛠️ Troubleshooting (সমস্যা সমাধান)

### Problem 1: "MAIN_BOT_UID not set" error
**Solution:**
- `.env` file name ঠিক আছে কিনা চেক করুন (`.env.txt` হয়ে গেছে কিনা)
- File টি bot folder-এর main directory-তে আছে কিনা
- `MAIN_BOT_UID=` এর পরে value দিয়েছেন কিনা
- Space বা quotation marks ব্যবহার করেননি তো? (শুধু value লিখুন)

**সঠিক:**
```env
MAIN_BOT_UID=4245749321
```

**ভুল:**
```env
MAIN_BOT_UID = "4245749321"   ❌ (space এবং quotes আছে)
MAIN_BOT_UID                  ❌ (value নেই)
```

---

### Problem 2: "Module 'dotenv' not found"
**Solution:**
```bash
pip install python-dotenv
```

অথবা:
```bash
pip install -r requirements.txt
```

---

### Problem 3: `.env` file দেখা যাচ্ছে না
**Reason:** Hidden file হতে পারে (যেহেতু `.` দিয়ে শুরু)

**Solution:**

**Windows এ:**
- File Explorer → View → Show hidden files

**Linux/Mac এ:**
```bash
ls -la
```

---

### Problem 4: Credentials কাজ করছে না
**Check করুন:**
1. UID এবং Password সঠিক আছে কিনা
2. Password encrypted format-এ আছে কিনা
3. Extra spaces নেই তো?
4. File encoding UTF-8 আছে কিনা

---

## 🔒 Security Tips (নিরাপত্তা টিপস)

### ✅ করুন (DO):
1. `.env` file সবসময় local computer-এ রাখুন
2. Backup নিয়ে রাখুন (secure জায়গায়)
3. `.gitignore`-এ `.env` আছে কিনা verify করুন
4. Strong passwords use করুন

### ❌ করবেন না (DON'T):
1. GitHub/GitLab-এ `.env` upload করবেন না
2. Screenshot শেয়ার করার সময় credentials দেখা যাচ্ছে কিনা check করুন
3. কারো সাথে `.env` file শেয়ার করবেন না
4. Public folder-এ রাখবেন না

---

## 📝 Example `.env` File

এরকম দেখতে হবে আপনার `.env` file:

```env
# ═══════════════════════════════════════════
# FREE FIRE BOT - Environment Configuration
# ═══════════════════════════════════════════

# Main Bot Credentials (Required)
MAIN_BOT_UID=4245749321
MAIN_BOT_PASSWORD=71496B76FB9E4BA2C14F80D7A75A5DD25F75793F267E4C21B73D662881404ED1

# API Token (Optional)
FF_API_TOKEN=your_token_here_if_you_have

# Settings (Optional)
DEFAULT_REGION=BD
WEB_PORT=5000
```

---

## 🔄 Different Environments এর জন্য

যদি multiple environments use করেন (যেমন: testing, production):

**Development/Testing:**
```env
# .env.development
MAIN_BOT_UID=test_account_uid
MAIN_BOT_PASSWORD=test_password
```

**Production:**
```env
# .env.production
MAIN_BOT_UID=main_account_uid
MAIN_BOT_PASSWORD=main_password
```

---

## ❓ FAQs (প্রায়ই জিজ্ঞাসিত প্রশ্ন)

### Q1: `.env` না থাকলে কি bot চলবে?
**A:** হ্যাঁ, কিন্তু আপনাকে code-এ (`main.py`) credentials manually দিতে হবে।

### Q2: Multiple bots run করতে চাই, কিভাবে করব?
**A:** Like bot accounts এর জন্য `like_bot_accounts.py` file use করুন। Main bot এর জন্য `.env`-এ শুধু একটা credential থাকবে।

### Q3: `.env` file accidentally delete হয়ে গেলে কি করব?
**A:** `.env.example` থেকে আবার তৈরি করুন এবং নতুন credentials দিন। (এজন্যই backup রাখা জরুরী!)

### Q4: Password plain text-এ দিলে কি হবে?
**A:** কাজ নাও করতে পারে। Free Fire encrypted password চায়। আপনার password encrypt করা লাগবে।

---

## 📞 Help & Support

যদি আরও সাহায্য লাগে:
1. `LOCAL_SETUP_GUIDE_BANGLA.md` দেখুন
2. `README.md` পড়ুন
3. Error message Google-এ search করুন

---

## ✅ Quick Checklist

Setup সম্পূর্ণ করার আগে চেক করুন:

- [ ] `.env.example` কপি করে `.env` তৈরি করেছি
- [ ] `MAIN_BOT_UID` দিয়েছি
- [ ] `MAIN_BOT_PASSWORD` দিয়েছি
- [ ] File save করেছি
- [ ] File name ঠিক আছে (`.env`, not `.env.txt`)
- [ ] Bot folder-এর main directory-তে আছে
- [ ] `python-dotenv` install করেছি
- [ ] `.gitignore`-এ `.env` আছে

সব ঠিক থাকলে bot run করুন! 🚀

---

**Good Luck! আপনার bot setup successful হোক!** 🎉
