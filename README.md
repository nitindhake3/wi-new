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

### 💻 Local Automated Daily Submission (Recommended for 100% Reliability)

To run the automation locally on your laptop automatically without any Google Cloud session expirations:

1. **One-Time Login**:
   Double-click `login_setup.bat` (or run `python main.py --setup-auth`).
   - A browser window opens.
   - Log into your `nitin.dhake.s73@kalvium.community` Google Account.
   - Return to the terminal and press **ENTER**.
   - Your session is permanently saved to `browser_profile/`.

2. **Register Daily Windows Schedule**:
   Double-click `setup_windows_scheduler.bat`.
   - Automatically registers `DailyKalviumWIFormBot` in Windows Task Scheduler.
   - Runs every day at **11:00 AM IST** silently in the background (`pythonw.exe`).
   - Automatically catches up if your laptop was closed/off at 11:00 AM when you next power on!

3. **Manual / Instant Test**:
   Double-click `run_bot.bat` anytime to test immediate form submission.

---

### ☁️ Cloud GitHub Actions Daily Submission (Optional Alternative)

If you also want GitHub Actions to run the bot in the cloud at 11:00 AM:

1. Run `python print_secret.py` to copy your Base64 cookie string.
2. In GitHub ➔ **Settings** ➔ **Secrets and variables** ➔ **Actions**, add:
   - `AUTH_JSON`: Pasted Base64 string.
   - `AUTH_PASSWORD`: Your Google account password *(enables automated re-authentication if cookies expire)*.
3. In GitHub ➔ **Actions**, click **Daily Google Form Auto-Fill Bot** ➔ **Run workflow**.

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
