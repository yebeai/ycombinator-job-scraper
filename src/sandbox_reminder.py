"""
Twilio Sandbox Keep-Alive

Uses Selenium + Brave to send 'join safety-pig' to the Twilio sandbox number
via WhatsApp Web, keeping the free tier session active (expires after 72 hours).

First run: Will show QR code - scan with your phone to log in.
Subsequent runs: Uses saved session (no QR needed).
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Twilio sandbox WhatsApp number (public number from Twilio docs)
TWILIO_SANDBOX_NUMBER = "14155238886"

# Directory to store WhatsApp Web session
PROFILE_DIR = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/whatsapp_profile")


def setup_driver():
    """Set up Brave browser with Selenium (reuses pattern from scraper.py)."""
    options = Options()
    options.binary_location = "/usr/bin/brave"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    # Uncomment for headless after first login:
    # options.add_argument("--headless=new")

    return webdriver.Chrome(options=options)


def send_sandbox_join():
    """
    Send 'join safety-pig' to Twilio sandbox via WhatsApp Web.
    """
    driver = None
    try:
        logger.info("Starting Brave with WhatsApp Web...")
        driver = setup_driver()

        # Open WhatsApp Web with the Twilio sandbox number
        url = f"https://web.whatsapp.com/send?phone={TWILIO_SANDBOX_NUMBER}&text=join%20safety-pig"
        driver.get(url)

        logger.info("Waiting for WhatsApp Web to load...")
        logger.info("If first run, scan QR code with your phone within 5 minutes.")

        # Wait for message input box (indicates logged in and chat loaded)
        wait = WebDriverWait(driver, 300)  # 5 min timeout for QR scan
        input_box = wait.until(EC.presence_of_element_located((
            By.XPATH, '//div[@contenteditable="true"][@data-tab="10"] | //footer//div[@contenteditable="true"]'
        )))

        logger.info("WhatsApp Web loaded. Sending message...")
        time.sleep(2)  # Brief pause for stability

        # Press Enter to send the pre-filled message
        input_box.send_keys(Keys.ENTER)

        logger.info("Message sent! Waiting for confirmation...")
        time.sleep(5)  # Wait for message to be sent

        logger.info("'join safety-pig' sent to Twilio sandbox successfully!")
        return True

    except Exception as e:
        logger.error(f"Failed to send message: {str(e)}")
        return False

    finally:
        if driver:
            driver.quit()


def main():
    logger.info("Starting Twilio sandbox keep-alive via Selenium")

    success = send_sandbox_join()

    if success:
        logger.info("Sandbox join completed successfully")
    else:
        logger.error("Sandbox join failed")


if __name__ == "__main__":
    main()
