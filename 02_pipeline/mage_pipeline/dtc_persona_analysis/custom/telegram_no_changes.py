if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import requests
import sys
import os

@custom
def transform_custom(data, *args, **kwargs):

    token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    message = os.environ.get('MESSAGE_NODRIFT')
    
    # args: The output from any upstream parent blocks (if applicable)

    # The URL for the sendMessage method of the Telegram Bot API
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # The payload to be sent in the request
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'  # Optional: for message formatting (e.g., *bold*, _italic_)
    }

    try:
        # Send the request
        response = requests.post(url, data=payload)
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        print("Message sent successfully!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
        return None

    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
