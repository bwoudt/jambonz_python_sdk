# example_webhook.py
from quart import Quart, request, jsonify
from jambonz_sdk import WebhookResponse, validate_webhook
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env
load_dotenv()

# Initialize the Quart app
app = Quart(__name__)

# Load configuration from environment variables
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('HTTP_PORT', 3000))
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')  # This can be None
LOGLEVEL = os.getenv('LOGLEVEL', 'INFO').upper()
NODE_ENV = os.getenv('NODE_ENV', 'production')
HTTP_USERNAME = os.getenv('HTTP_USERNAME')
HTTP_PASSWORD = os.getenv('HTTP_PASSWORD')

# Set up logging with the specified log level
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)

@app.route('/hello-world', methods=['POST'])
async def hello_world():
    # Extract JSON payload from the incoming request
    data = await request.json
    signature = request.headers.get('X-Signature', '')

    # Validate the incoming webhook if a secret is provided
    if WEBHOOK_SECRET:
        if not validate_webhook(WEBHOOK_SECRET, signature, data):
            logger.warning("Invalid webhook signature")
            return jsonify({"error": "Invalid signature"}), 403

    # Optional basic authentication
    if HTTP_USERNAME and HTTP_PASSWORD:
        auth = request.authorization
        if not auth or auth.username != HTTP_USERNAME or auth.password != HTTP_PASSWORD:
            logger.warning("Unauthorized access attempt")
            return jsonify({"error": "Unauthorized"}), 401

    logger.info(f"Received data: {data}")

    # Create a WebhookResponse with say and hangup commands
    response = WebhookResponse()
    response.say(
        "<speak><prosody volume='loud'>Hi there,</prosody> and welcome to Jambonz!</speak>"
    ).pause(length=1.5).hangup()

    # Return the response as JSON
    return jsonify(response.verbs), 200

if __name__ == '__main__':
    # Run the app with the specified host and port
    app.run(host=HOST, port=PORT)
