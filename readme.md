# Jambonz Python SDK

This repository provides a Python SDK for interacting with Jambonz, both for handling webhooks and making REST API calls. The SDK makes it easy to build telephony applications using Jambonz's powerful CPaaS capabilities.

## Features

- Easy-to-use `WebhookResponse` class for building responses to Jambonz webhooks.
- `JambonzClient` for interacting with the Jambonz REST API, including creating, updating, and managing calls.
- Webhook validation using HMAC-SHA256 to ensure secure interactions.
- Support for all common Jambonz verbs, including `say`, `play`, `gather`, `pause`, `hangup`, `dial`, `redirect`, `leave`, and more.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/bwoudt/jambonz_python_sdk.git
    cd jambonz_python_sdk
    ```

2. Set up a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Install the SDK locally:

    ```bash
    pip install -e .
    ```

## Configuration

Create a `.env` file in the root directory with the following content:

```ini
# Environment settings
NODE_ENV=production
LOGLEVEL=info

# HTTP server settings
HOST=0.0.0.0
HTTP_PORT=3000

# WebSocket URL including port
JAMBONZ_WEBSOCKET_URL=

# Jambonz API credentials
JAMBONZ_ACCOUNT_SID=<YOUR_JAMBONZ_ACCOUNT_SID>
JAMBONZ_API_KEY=<YOUR_JAMBONZ_API_KEY>
JAMBONZ_REST_API_BASE_URL=https://api.jambonz.com/v1

# Optional webhook secret for validating incoming requests (can be left empty)
WEBHOOK_SECRET=<YOUR_WEBHOOK_SECRET>

# Optional basic auth credentials for webhook security
HTTP_USERNAME=<YOUR_USERNAME>
HTTP_PASSWORD=<YOUR_PASSWORD>
```

Replace the placeholders with your Jambonz account details. WEBHOOK_SECRET, HTTP_USERNAME, and HTTP_PASSWORD are optional.

### Usage
1. Handling Webhooks
Use the example_webhook.py script to create a server that listens for incoming webhooks from Jambonz:

```bash
python examples/example_webhook.py
```
This will start a server on http://0.0.0.0:3000 that handles webhooks and responds with a text-to-speech message.

2. Making REST API Calls
Use the example_rest.py script to interact with the Jambonz REST API:

```bash
python examples/example_rest.py
```
This script demonstrates how to create a new call, check its status, and end the call.

### SDK Structure
The project is structured as follows:

```bash
jambonz_python_sdk/
├── jambonz/
│   ├── __init__.py         # Imports main classes and functions
│   ├── client.py           # Contains JambonzClient for REST API interactions
│   ├── webhook_response.py # Contains WebhookResponse class for building webhook responses
│   ├── utils.py            # Contains utility functions like validate_webhook
├── examples/
│   ├── example_webhook.py  # Example script for handling webhooks
│   ├── example_rest.py     # Example script for making REST API calls
├── .env                    # Environment variables for configuration (not included in the repository)
├── LICENSE                 # License information
├── README.md               # This file
└── requirements.txt        # Required Python packages
```
### Example Code
Example: Handling a Webhook
```python
from quart import Quart, request, jsonify
from jambonz import WebhookResponse, validate_webhook
import os

app = Quart(__name__)
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

@app.route('/hello-world', methods=['POST'])
async def hello_world():
    data = await request.json
    signature = request.headers.get('X-Signature', '')

    # Validate the webhook if a secret is set
    if WEBHOOK_SECRET and not validate_webhook(WEBHOOK_SECRET, signature, data):
        return jsonify({"error": "Invalid signature"}), 403

    response = WebhookResponse()
    response.say("Hi there! Welcome to Jambonz with Python.").pause(1.5).hangup()
    return jsonify(response.verbs), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
```
Example: Using the JambonzClient
```python
from jambonz import JambonzClient
import os

client = JambonzClient(
    account_sid=os.getenv('JAMBONZ_ACCOUNT_SID'),
    api_key=os.getenv('JAMBONZ_API_KEY'),
    base_url=os.getenv('JAMBONZ_REST_API_BASE_URL', 'https://api.jambonz.com/v1')
)

call_data = {
    "from": "+1234567890",
    "to": "+0987654321",
    "application_sid": "your-application-sid"
}

# Create a new call
response = client.create_call(call_data)
print(f"Call created with SID: {response['sid']}")
```
### Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for new features, bug fixes, or improvements.

License:
This project is licensed under the MIT License - see the LICENSE file for details.