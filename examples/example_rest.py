# example_rest.py
from jambonz_sdk import JambonzClient
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env
load_dotenv()

# Load environment variables for authentication
ACCOUNT_SID = os.getenv('JAMBONZ_ACCOUNT_SID')
API_KEY = os.getenv('JAMBONZ_API_KEY')
BASE_URL = os.getenv('JAMBONZ_REST_API_BASE_URL', 'https://jambonz.cloud')

# Initialize the client
client = JambonzClient(
    account_sid=ACCOUNT_SID,
    api_key=API_KEY,
    base_url=BASE_URL
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_and_manage_call():
    # Create a new call
    call_data = {
        "from": "+1234567890",
        "to": "+0987654321",
        "application_sid": "your-application-sid"
    }
    try:
        # Create the call
        response = client.create_call(call_data)
        call_sid = response.get('sid')
        logger.info(f"Call created with SID: {call_sid}")

        # Get the call status
        status = client.get_call_status(call_sid)
        logger.info(f"Call status: {status}")

        # End the call
        client.end_call(call_sid)
        logger.info("Call successfully ended.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    create_and_manage_call()
