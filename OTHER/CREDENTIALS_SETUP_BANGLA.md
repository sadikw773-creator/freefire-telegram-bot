# 🔐 CREDENTIALS SETUP GUIDE (সরাসরি Code-এ)

## 📋 দুইটা Option আছে

### ✅ Option 1: সরাসরি `main.py` তে দিন (সবচেয়ে সহজ!)

**File**: `main.py` (Line 56-57 এর কাছে)

```python
# এখানে আপনার credentials দিন:
HARDCODED_BOT_UID = "আপনার_বট_UID"
HARDCODED_BOT_PASSWORD = "আপনার_বট_পাসওয়ার্ড"
```

**উদাহরণ:**
```python
HARDCODED_BOT_UID = "4245749321"
HARDCODED_BOT_PASSWORD = "71496B76FB9E4BA2C14F80D7A75A5DD25F75793F267E4C21B73D662881404ED1"
```

এখন save করে bot run করুন:
```bash
python main.py
```

**✅ সুবিধা:**
- সবচেয়ে সহজ
- `.env` file লাগবে না
- `python-dotenv` install করার দরকার নেই

**⚠️ সাবধানতা:**
- GitHub-এ upload করার আগে credentials **অবশ্যই** remove করবেন!
- Code কারো সাথে share করার আগে credentials মুছে দিন

---

### ✅ Option 2: `.env` File ব্যবহার করুন (More Secure)

যদি Option 1 এ কিছু না দেন, তাহলে automatic `.env` file থেকে পড়বে।

**File**: `.env`
```env
MAIN_BOT_UID=আপনার_বট_UID
MAIN_BOT_PASSWORD=আপনার_বট_পাসওয়ার্ড
```

বিস্তারিত: [`ENV_SETUP_GUIDE_BANGLA.md`](ENV_SETUP_GUIDE_BANGLA.md) দেখুন

---

## 🚀 Quick Start (সরাসরি Code-এ)

### Step 1: `main.py` Open করুন

Text editor দিয়ে `main.py` file open করুন।

### Step 2: Line 56-57 খুঁজুন

এই লাইনগুলো দেখবেন:
```python
HARDCODED_BOT_UID = ""
HARDCODED_BOT_PASSWORD = ""
```

### Step 3: আপনার Credentials দিন

```python
HARDCODED_BOT_UID = "4245749321"
HARDCODED_BOT_PASSWORD = "71496B76FB9E4BA2C14F80D7A75A5DD25F75793F267E4C21B73D662881404ED1"
```

⚠️ **গুরুত্বপূর্ণ**: Quote marks (`""`) এর ভিতরে দিতে হবে!

### Step 4: File Save করুন

`Ctrl + S` (Windows/Linux) বা `Cmd + S` (Mac)

### Step 5: Bot Run করুন

```bash
python main.py
```

---

## ✅ কিভাবে বুঝবেন সঠিকভাবে Set হয়েছে?

Bot start করার পর terminal-এ দেখবেন:

**✅ সফল (Success):**
```
[INFO] Bot UID: 4245749321
[INFO] Authenticating...
[SUCCESS] Login successful!
```

**❌ ভুল (Failed):**
```
[ERROR] Bot credentials not set!
[ERROR] Please set HARDCODED_BOT_UID and HARDCODED_BOT_PASSWORD
```

অথবা:
```
[ERROR] Authentication failed
[ERROR] Invalid credentials
```

---

## 🔄 কোন Option ব্যবহার হচ্ছে চেক করুন

Bot automatic এভাবে decide করে:

```
1. HARDCODED_BOT_UID খালি না?
   ├─ YES → Hardcoded credentials use করবে
   └─ NO → .env file থেকে পড়বে
```

---

## 🛠️ Troubleshooting

### Problem 1: Credentials কাজ করছে না

**Check করুন:**
```python
# ✅ সঠিক (Correct):
HARDCODED_BOT_UID = "4245749321"

# ❌ ভুল (Wrong):
HARDCODED_BOT_UID = 4245749321       # Quote marks নেই
HARDCODED_BOT_UID = "4245749321      # শেষে quote marks নেই
HARDCODED_BOT_UID = ""               # খালি
```

### Problem 2: Password format ভুল

**Password encrypted format এ হতে হবে!**

```python
# ✅ সঠিক - Encrypted (64 characters hex):
HARDCODED_BOT_PASSWORD = "71496B76FB9E4BA2C14F80D7A75A5DD25F75793F267E4C21B73D662881404ED1"

# ❌ ভুল - Plain text password:
HARDCODED_BOT_PASSWORD = "mypassword123"
```

### Problem 3: Indentation error

Python-এ indentation (spacing) ঠিক রাখতে হয়:

```python
# ✅ সঠিক:
HARDCODED_BOT_UID = "4245749321"

# ❌ ভুল (extra space):
    HARDCODED_BOT_UID = "4245749321"
```

---

## 🔒 Security Best Practices

### ✅ করুন (DO):
1. Local computer এ development এর সময় use করুন
2. Code run করার আগে credentials check করুন
3. Backup রাখুন (secure জায়গায়)

### ❌ করবেন না (DON'T):
1. **GitHub/GitLab-এ push করবেন না credentials সহ!**
2. Screenshot share করার সময় credentials দেখা যাচ্ছে কিনা check করুন
3. Code publicly share করার আগে credentials remove করুন
4. Production server এ hardcoded credentials use করবেন না

---

## 🔄 GitHub এ Upload করার আগে

### Option A: Credentials Remove করুন

```python
# খালি করে দিন:
HARDCODED_BOT_UID = ""
HARDCODED_BOT_PASSWORD = ""
```

### Option B: `.gitignore` check করুন

যদি `.env` file use করেন, তাহলে `.gitignore` এ `.env` আছে কিনা verify করুন:

```gitignore
# .gitignore file
.env
.env.local
```

---

## 💡 Best Practice Recommendation

**Local Development:** Option 1 (Hardcoded) - সবচেয়ে সহজ

**Production/Sharing:** Option 2 (.env file) - সবচেয়ে secure

**Mixed Approach:** 
- Development: Hardcoded use করুন
- Push করার আগে: Hardcoded empty করুন, `.env` এ credentials রাখুন
- `.gitignore` এ `.env` add করুন

---

## 📋 Example Setup

**`main.py` (Line 56-57):**
```python
# আপনার actual credentials:
HARDCODED_BOT_UID = "4245749321"
HARDCODED_BOT_PASSWORD = "71496B76FB9E4BA2C14F80D7A75A5DD25F75793F267E4C21B73D662881404ED1"
```

**Run:**
```bash
python main.py
```

**Output:**
```
╔═══════════════════════════════════════╗
║     FREE FIRE TCP BOT - EMOTE         ║
╚═══════════════════════════════════════╝

[INFO] Bot UID: 4245749321
[INFO] Authenticating...
[SUCCESS] Login successful!
[INFO] Connected to Free Fire servers
[INFO] Bot is ready! Send /help for commands
```

---

## ❓ FAQs

### Q1: দুইটা option-ই দিলে কোনটা use হবে?
**A:** Hardcoded credentials প্রথমে check করে। সেটা থাকলে সেটা use করবে।

### Q2: Password কোথায় পাবো?
**A:** Free Fire account এর encrypted password লাগবে। Plain text password কাজ করবে না।

### Q3: Multiple bots run করতে চাই?
**A:** Main bot শুধু একটা। Multiple like bots এর জন্য `like_bot_accounts.py` use করুন।

### Q4: Credentials change করতে চাই?
**A:** `main.py` edit করে নতুন credentials দিন এবং bot restart করুন।

---

**সহজ হয়েছে! এখন শুধু credentials দিয়ে run করুন!** 🚀
