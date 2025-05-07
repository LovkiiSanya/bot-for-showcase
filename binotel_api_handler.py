"""
binotel_api_handler.py

This module provides a Python interface for interacting with the Binotel SmartCRM API.
It supports customer creation, note addition, label updates, and authentication.

Environment Variables:
    - API_KEY: Your Binotel public API key.
    - API_SECRET: Your Binotel secret API key.
    - BINOTEL_EMAIL: Login email for Binotel SmartCRM dashboard.
    - BINOTEL_PASSWORD: Login password for Binotel SmartCRM dashboard.

Classes:
    - BinotelAPI: Handles authenticated session and operations with the Binotel API.

Functions:
    - create_note_for_patient: Utility to quickly create a note in Binotel for a patient.
"""

import os
import requests

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BINOTEL_EMAIL = os.getenv("BINOTEL_EMAIL")
BINOTEL_PASSWORD = os.getenv("BINOTEL_PASSWORD")


class BinotelAPI:
    """
    Handles session management and communication with the Binotel API.

    Methods:
        - login(): Authenticates the session using credentials.
        - create_customer(): Creates a new customer entry in Binotel.
        - create_note(): Adds a note to a customer's record.
        - update_customer_labels(): Updates or assigns tags/labels to a customer.
        - create_client_with_tag(): Creates a client and assigns tags immediately.
    """

    LOGIN_URL = "https://my.binotel.ua/"
    NOTE_URL = "https://my.binotel.ua/b/smartcrm/note"
    AUTH_URL = "https://my.binotel.ua/b/smartcrm/auth/callback?state=https://my.binotel.ua/f/smartcrm/"
    CUSTOMER_URL = "https://api.binotel.com/api/4.0/customers/create.json"
    UPDATE_LABEL_URL = "https://my.binotel.ua/b/smartcrm/client/"
    CLIENT_URL = "https://my.binotel.ua/b/smartcrm/client"

    def __init__(self, email, password, api_key, api_secret):
        """
        Initialize the BinotelAPI class with credentials and API keys.

        Args:
            email (str): Binotel login email.
            password (str): Binotel login password.
            api_key (str): Binotel API public key.
            api_secret (str): Binotel API secret key.
        """
        self.session = requests.Session()
        self.email = email
        self.password = password
        self.api_key = api_key
        self.api_secret = api_secret
        self.authenticated = False

    def login(self):
        """
        Authenticates with Binotel and sets session cookies.

        Raises:
            Exception: If login fails (non-200 status code).
        """
        login_data = {
            "logining[email]": self.email,
            "logining[password]": self.password,
            "logining[submit]": "",
        }
        response = self.session.post(self.LOGIN_URL, data=login_data)
        if response.status_code == 200:
            self.authenticated = True
            self.session.get(self.AUTH_URL)
        else:
            raise Exception("Binotel login failed: {}".format(response.status_code))

    def create_customer(self, name, phone, email, description, internal_number):
        """
        Creates a customer in Binotel and returns the customer ID.

        Args:
            name (str): Full name of the customer.
            phone (str): Phone number (e.g., 380671234567).
            email (str): Email address of the customer.
            description (str): Description/note about the customer.
            internal_number (str): Assigned internal employee number.

        Returns:
            str: Binotel customer ID.

        Raises:
            Exception: If the request fails.
        """
        if not self.authenticated:
            self.login()

        payload = {
            "key": self.api_key,
            "secret": self.api_secret,
            "name": name,
            "numbers": [phone],
            "description": description,
            "email": email,
            "assignedToEmployee": {"internalNumber": internal_number},
        }

        response = self.session.post(self.CUSTOMER_URL, json=payload)
        if response.status_code == 200:
            return response.json().get("customerID")
        raise Exception("Failed to create customer: {}".format(response.status_code))

    def create_note(self, customer_id, comment):
        """
        Adds a note to a Binotel customer.

        Args:
            customer_id (str): Binotel customer ID.
            comment (str): Note/comment content.

        Returns:
            dict: JSON response from Binotel.

        Raises:
            Exception: If note creation fails.
        """
        if not self.authenticated:
            self.login()

        response = self.session.post(
            self.NOTE_URL,
            headers={"x-requested-with": "XMLHttpRequest"},
            data={
                "id": "0",
                "objectId": customer_id,
                "type": "client",
                "comment": comment,
            },
        )
        if response.status_code == 200:
            return response.json()
        raise Exception("Failed to create note: {}".format(response.status_code))

    def update_customer_labels(self, customer_id, email, tags):
        """
        Updates or assigns tags (labels) to a customer.

        Args:
            customer_id (str or int): Binotel customer ID.
            email (str): Email associated with the customer.
            tags (list): List of tag dictionaries (e.g., [{"id": 1, "name": "VIP"}]).

        Returns:
            dict: JSON response from Binotel.

        Raises:
            Exception: If the update fails.
        """
        if not self.authenticated:
            self.login()

        url = "{}{}".format(self.UPDATE_LABEL_URL, customer_id)
        params = {"_method": "PUT"}
        json_data = {
            "id": customer_id,
            "email": email,
            "tags": tags,
        }

        headers = {
            "content-type": "application/json",
            "x-requested-with": "XMLHttpRequest",
        }

        response = self.session.post(url, params=params, headers=headers, json=json_data)
        if response.status_code == 200:
            return response.json()
        raise Exception("Failed to update labels: {}".format(response.status_code))

    def create_client_with_tag(self, name, phone, tag_id, tag_name):
        """
        Creates a client with an assigned tag.

        Args:
            name (str): Customer name.
            phone (str): Phone number (digits only).
            tag_id (int): Tag ID from Binotel system.
            tag_name (str): Tag name.

        Returns:
            dict: JSON response with customer info.

        Raises:
            Exception: If the operation fails.
        """
        if not self.authenticated:
            self.login()

        json_data = {
            "id": 0,
            "assignedToEmployeeID": 0,
            "name": name,
            "numbers": [{"id": 0, "value": phone}],
            "tags": [{"id": tag_id, "name": tag_name}],
        }

        headers = {
            "content-type": "application/json",
            "x-requested-with": "XMLHttpRequest",
        }

        response = self.session.post(self.CLIENT_URL, headers=headers, json=json_data)
        if response.status_code == 200:
            return response.json()
        raise Exception(
            "Failed to create client with tag: {} | {}".format(
                response.status_code, response.text
            )
        )


def create_note_for_patient(note_input, note_text, customer_id, chat_id, bot):
    """
    Utility function to create a note in Binotel for a specific customer.

    Args:
        note_input (str): Label or prefix for the note.
        note_text (str): The actual note content.
        customer_id (str): Binotel customer ID.
        chat_id (int): Telegram chat ID of the user.
        bot (TeleBot): Bot instance to send error messages if any occur.

    Returns:
        None
    """
    try:
        binotel = BinotelAPI(
            email=BINOTEL_EMAIL,
            password=BINOTEL_PASSWORD,
            api_key=API_KEY,
            api_secret=API_SECRET,
        )
        comment = "{} {}".format(note_input, note_text)
        binotel.create_note(customer_id, comment)
    except Exception as e:
        bot.send_message(chat_id, "Помилка Binotel: {}".format(e))


# Optional default instance for direct usage
binotel = BinotelAPI(
    email=BINOTEL_EMAIL,
    password=BINOTEL_PASSWORD,
    api_key=API_KEY,
    api_secret=API_SECRET,
)
