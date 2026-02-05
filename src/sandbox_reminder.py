"""
Twilio Sandbox Reminder

Sends a WhatsApp reminder to re-join the Twilio sandbox.
Free tier requires you to send 'join safety-pig' every 72 hours
to keep your WhatsApp automation working.

This script runs every 71 hours to remind you before expiration.
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


def send_sandbox_reminder():
    """
    Send a reminder to rejoin the Twilio WhatsApp sandbox.

    The Twilio free tier sandbox expires after 72 hours.
    You must manually send 'join safety-pig' to the Twilio
    WhatsApp number to keep your automation working.
    """
    reminder_message = (
        "TWILIO SANDBOX REMINDER\n\n"
        "Your Twilio WhatsApp sandbox session expires soon!\n\n"
        "ACTION REQUIRED: Send 'join safety-pig' to the Twilio "
        "WhatsApp number to keep your automation working.\n\n"
        "WHY: The Twilio free tier only allows 72 hours of sandbox "
        "access. You must manually resend the join message to "
        "reactivate your WhatsApp automation.\n\n"
        "This reminder is sent every 71 hours to give you time "
        "before expiration."
    )

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=reminder_message,
            from_=f'whatsapp:{TWILIO_PHONE_NUMBER}',
            to=f'whatsapp:{YOUR_PHONE_NUMBER}'
        )

        logger.info(f"Sandbox reminder sent successfully: {message.sid}")
        return True

    except Exception as e:
        logger.error(f"Failed to send sandbox reminder: {str(e)}")
        return False


def main():
    logger.info("Starting Twilio sandbox reminder")

    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, YOUR_PHONE_NUMBER]):
        logger.error("Missing required environment variables")
        return

    success = send_sandbox_reminder()

    if success:
        logger.info("Sandbox reminder completed successfully")
    else:
        logger.error("Sandbox reminder failed")


if __name__ == "__main__":
    main()
