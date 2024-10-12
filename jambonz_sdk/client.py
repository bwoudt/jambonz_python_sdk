import requests

class JambonzClient:
    def __init__(self, account_sid, api_key, base_url='https://jambonz.cloud'):
        """
        Initializes the JambonzClient with account credentials and base URL.
        
        Args:
            account_sid (str): The account SID for Jambonz.
            api_key (str): The API key for Jambonz.
            base_url (str): The base URL for the Jambonz API.
        """
        self.account_sid = account_sid
        self.api_key = api_key
        self.base_url = base_url

    def _get_headers(self):
        """Generates headers for API requests."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _handle_response(self, response):
        """
        Handles the response from the API, raising exceptions for errors.
        
        Args:
            response (requests.Response): The response object to handle.
        
        Returns:
            dict: The JSON response from the API if successful.
        
        Raises:
            Exception: If the response status code indicates an error.
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            error_message = f"API request failed: {err}, Response: {response.text}"
            raise Exception(error_message)
        
        return response.json()

    def update_call(self, call_sid, data):
        """
        Updates an existing call with the given data.
        
        Args:
            call_sid (str): The SID of the call to update.
            data (dict): The data to update the call with.
        
        Returns:
            dict: The updated call information.
        """
        url = f'{self.base_url}/v1/calls/{call_sid}'
        response = requests.patch(url, json=data, headers=self._get_headers())
        return self._handle_response(response)

    def create_call(self, data):
        """
        Creates a new call with the given data.
        
        Args:
            data (dict): The data for creating the call.
        
        Returns:
            dict: The created call information.
        """
        url = f'{self.base_url}/v1/calls'
        response = requests.post(url, json=data, headers=self._get_headers())
        return self._handle_response(response)

    def end_call(self, call_sid):
        """
        Ends an existing call.
        
        Args:
            call_sid (str): The SID of the call to end.
        
        Returns:
            dict: Information about the ended call.
        """
        url = f'{self.base_url}/v1/calls/{call_sid}'
        response = requests.delete(url, headers=self._get_headers())
        return self._handle_response(response)

    def get_call_status(self, call_sid):
        """
        Retrieves the status of a specific call.
        
        Args:
            call_sid (str): The SID of the call to retrieve the status for.
        
        Returns:
            dict: The call status information.
        """
        url = f'{self.base_url}/v1/calls/{call_sid}'
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
