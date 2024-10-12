import hmac
import hashlib
import json

def validate_webhook(secret, signature, payload):
    """
    Validates a Jambonz webhook request using HMAC-SHA256.

    Args:
        secret (str): The secret key used to verify the signature.
        signature (str): The HMAC-SHA256 signature provided by the webhook.
        payload (dict): The JSON payload of the webhook as a dictionary.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    try:
        # Convert the payload back to JSON string for hashing
        payload_json = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)

        # Create the HMAC-SHA256 signature using the secret and payload
        computed_signature = hmac.new(
            key=secret.encode('utf-8'),
            msg=payload_json.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        # Compare the computed signature with the one provided in a constant-time manner
        return hmac.compare_digest(computed_signature, signature)
    except Exception as e:
        # Log the error if needed
        print(f"Error validating webhook: {e}")
        return False
