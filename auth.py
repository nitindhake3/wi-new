import json
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

from logger import get_logger

logger = get_logger("auth")

AUTH_FILE = Path("auth.json")
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

CHROMIUM_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-infobars",
    "--window-size=1280,900",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--no-first-run",
    "--no-service-autorun",
    "--password-store=basic",
]

STEALTH_INIT_SCRIPT = """
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.chrome = { runtime: {} };
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
"""

BROWSER_PROFILE_DIR = Path("browser_profile")

def is_auth_valid(auth_path: Path = AUTH_FILE) -> bool:
    """Checks whether either the browser_profile exists or auth.json contains stored cookies."""
    if (BROWSER_PROFILE_DIR / "Default").exists():
        return True

    if not auth_path.exists():
        logger.warning(f"Auth file '{auth_path}' does not exist.")
        return False

    try:
        with open(auth_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        cookies = data.get("cookies", [])
        origins = data.get("origins", [])

        if not cookies and not origins:
            logger.warning(f"Auth file '{auth_path}' contains no cookies or origins.")
            return False

        logger.info(f"Auth file '{auth_path}' is present with {len(cookies)} cookies.")
        return True
    except Exception as e:
        logger.error(f"Failed to read auth file '{auth_path}': {e}")
        return False

def setup_auth(auth_path: Path = AUTH_FILE, target_url: str = "https://accounts.google.com") -> bool:
    """
    Launches a headful browser for the user to log into their Google account.
    Saves the permanent profile to browser_profile/ and exports storage state to auth.json.
    """
    logger.info("=== Starting One-Time Google Authentication Setup ===")
    logger.info("A browser window will open. Please log into your Google Account.")

    BROWSER_PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(BROWSER_PROFILE_DIR.resolve()),
                channel="chrome",
                headless=False,
                args=CHROMIUM_ARGS,
                viewport={"width": 1280, "height": 800},
                locale="en-US",
                timezone_id="Asia/Kolkata",
            )
        except Exception:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(BROWSER_PROFILE_DIR.resolve()),
                headless=False,
                args=CHROMIUM_ARGS,
                viewport={"width": 1280, "height": 800},
                locale="en-US",
                timezone_id="Asia/Kolkata",
            )

        context.add_init_script(STEALTH_INIT_SCRIPT)
        page = context.pages[0] if context.pages else context.new_page()

        try:
            page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            logger.warning(f"Initial navigation notice: {e}")

        print("\n" + "=" * 70)
        print("ACTION REQUIRED: Log into your Google Account in the opened browser window.")
        print("Once you are logged in successfully and can see your Form or Google Dashboard,")
        print("return here and press ENTER to save your session state.")
        print("=" * 70 + "\n")

        try:
            input("Press ENTER when login is complete...")
        except KeyboardInterrupt:
            logger.warning("Authentication setup cancelled by user.")
            context.close()
            return False

        # Navigate to target form URL if available to ensure docs.google.com cookies are generated
        if target_url and "docs.google.com" in target_url:
            try:
                logger.info("Navigating to Google Form to capture form-specific session state...")
                page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
                try:
                    page.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    pass
                time.sleep(3)
            except Exception as e:
                logger.warning(f"Could not load form URL during auth setup: {e}")

        # Save storage state to auth.json as well
        try:
            context.storage_state(path=str(auth_path))
        except Exception as e:
            logger.warning(f"Could not export storage_state: {e}")

        context.close()

    if is_auth_valid(auth_path):
        logger.info(f"SUCCESS: Persistent profile and authentication session saved.")
        print(f"\nAuthentication session successfully saved!")
        print("Your browser session is permanently saved in 'browser_profile/' and 'auth.json'.")
        print("You can now run the bot or scheduler locally!\n")
        return True
    else:
        logger.error(f"FAILURE: Authentication was not saved correctly.")
        return False

if __name__ == "__main__":
    setup_auth()

