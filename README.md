# 🤖 Google Form Auto-Fill Bot (WI Daily Attendance)

Designed specifically for restricted Google Forms requiring Google account authentication (e.g. `@kalvium.community`), automatically submitting your form everyday at **11:00 AM IST** using GitHub Actions without requiring your laptop to be turned on.

---

## 👥 Setup Guide

Follow these simple steps to configure and run your automated Google Form submission bot:

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/nitindhake3/wi-new.git
cd wi-new
```

---

### Step 2: Install Local Dependencies

Set up Python and Playwright on your laptop (required only once to capture your login session):

```bash
# Install Python requirements
pip install -r requirements.txt

# Install Playwright Chromium browser
playwright install chromium
```

---

### Step 3: Configure Your Google Form (`config.json`)

Edit `config.json` with your Google Form URL, submit time, timezone, and answers:

```json
{
  "form_url": "https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform",
  "submit_time": "11:00",
  "timezone": "Asia/Kolkata",
  "answers": {
    "Email": "Record your.email@kalvium.community as the email to be included with my response",
    "A confirmation to start with - was today a working day for you?": "It was a working day, and I was present",
    "What were your key tasks for the day?": ".",
    "What challenges/problems did you solve today?": ".",
    "What challenges/problems you were NOT able to solve today and are planning to solve in upcoming days?": ".",
    "What is your plan for the next day of Simulated Work?": "."
  }
}
```

Commit and push your updated `config.json` to your GitHub repository:
```bash
git add config.json
git commit -m "Update config with my form details"
git push
```

---

### Step 4: One-Time Google Account Login Setup

Run the one-time authentication helper to log into your `@kalvium.community` account:

```bash
python main.py --setup-auth
```

1. A browser window will open loading your Google Form.
2. Log into your `@kalvium.community` Google Account.
3. Once your form is visible on screen, return to your terminal and press **ENTER**.
4. Your login cookies are safely saved to `auth.json` on your laptop.

---

### Step 5: Add Secrets to GitHub Repository Secrets

1. Run the secret helper script in your terminal to get your session cookie:
   ```bash
   python print_secret.py
   ```
2. Copy the single-line Base64 secret text printed on your screen.
3. Open your repository on **GitHub.com** ➔ **Settings** ➔ **Secrets and variables** ➔ **Actions**.
4. Click **New repository secret**:
   - **Name**: `AUTH_JSON`
   - **Value**: Paste your copied Base64 secret string.
5. *(Highly Recommended)* Add your Google Account password so the bot can **auto-reauthenticate** whenever Google session cookies expire:
   - **Name**: `AUTH_PASSWORD`
   - **Value**: Your `@kalvium.community` account password.
   *(This enables the bot to automatically click your account and solve the Google password challenge on GitHub Actions runners without failing!)*

---

### Step 6: Enable & Test your GitHub Action Workflow

1. Go to the **Actions** tab on your GitHub repository.
2. Select **Daily Google Form Auto-Fill Bot** from the left sidebar.
3. Click **Run workflow** ➔ **Run workflow** to test submission immediately.

---

### 💻 Bonus: Automated Local Daily Submission (Windows Task Scheduler)

If you also want your laptop to automatically submit the form locally every day at 11:00 AM IST (zero cloud session issues):
1. Double-click or run:
   ```cmd
   setup_windows_scheduler.bat
   ```
2. That's it! Windows will automatically execute the bot every day at 11:00 AM IST. If your laptop was closed/off at 11:00 AM, the bot will automatically detect the missed submission and catch up when you boot.

---

#### Quick Command to Re-Authenticate Manually (if not using AUTH_PASSWORD)
1. `python main.py --setup-auth`
2. Log into your `@kalvium.community` account in the browser that opens
3. Press **ENTER** in the terminal
4. `python print_secret.py`
5. Update `AUTH_JSON` in GitHub Secrets


## THE QUESTION'S WILL GET IN YOUR MIND❓ (FAQ)

<details>
<summary><b>What if Google says "session expired"?</b></summary>
Google session cookies expire periodically or when accessed from a new cloud IP (GitHub Actions runner). Simply re-run <code>python main.py --setup-auth</code> locally and update your <code>AUTH_JSON</code> secret on GitHub.
</details>

<details>
<summary><b>Does my laptop need to stay turned on?</b></summary>
<b>No!</b> GitHub Actions runs on GitHub's cloud servers. Your laptop can be turned off, asleep, or disconnected from the internet.
</details>

<details>
<summary><b>Is my Google password or login safe?</b></summary>
<b>Yes.</b> GitHub Repository Secrets are encrypted at rest by GitHub and masked in all workflow logs.
</details>

<details>
<summary><b>Where can I check if my form was submitted today?</b></summary>
Check the <b>Actions</b> tab of your GitHub repository. Every daily run will show a green checkmark (<code>✓</code>) along with execution logs.
</details>
