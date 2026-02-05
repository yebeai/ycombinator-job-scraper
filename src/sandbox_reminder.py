"""
Twilio Sandbox Keep-Alive

Sends a minimal ping to keep the Twilio WhatsApp sandbox session active.
The free tier expires after 72 hours of inactivity. This runs every 71 hours
to maintain the connection automatically.

Note: The Twilio API cannot send "join safety-pig" TO Twilio (that requires
your WhatsApp app). But outbound messages from the sandbox keep it active.
"""

from twilio.rest import Client
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
YOUR_PHONE_NUMBER = os.environ.get('YOUR_PHONE_NUMBER')


def send_keepalive_ping():
    """
    Send a minimal message to keep the Twilio sandbox session active.
    This prevents the 72-hour timeout on the free tier.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=".",
            from_=f'whatsapp:{TWILIO_PHONE_NUMBER}',
            to=f'whatsapp:{YOUR_PHONE_NUMBER}'
        )

        logger.info(f"Keep-alive ping sent: {message.sid}")
        return True

    except Exception as e:
        logger.error(f"Failed to send keep-alive ping: {str(e)}")
        return False


def main():
    logger.info("Starting Twilio sandbox keep-alive")

    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, YOUR_PHONE_NUMBER]):
        logger.error("Missing required environment variables")
        return

    success = send_keepalive_ping()

    if success:
        logger.info("Keep-alive completed successfully")
    else:
        logger.error("Keep-alive failed")


if __name__ == "__main__":
    main()
