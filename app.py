import json
import requests
from bs4 import BeautifulSoup
import re

def percentage_string_to_int(percentage_str):
    # Extract the numeric part of the percentage string
    match = re.match(r"(\d+(\.\d+)?)%", percentage_str.strip())
    if match:
        # Convert to float and then to integer
        return int(float(match.group(1)))
    else:
        raise ValueError(f"Invalid percentage string: {percentage_str}")


def send_get_request(url, params=None):
    try:
        # Send GET request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Print response content
        print("Response Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Content:", response.text)
        
        # Optionally, return the response object
        return response
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def read_settings(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def read_online_html_and_search_id(url, element_id):
    try:
        # Fetch the HTML content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for the element by its ID
        element = soup.find(class_=element_id)

        if element:
            print(f"Element with ID '{element_id}':")
            print(element.prettify())

            # Print the text content of the element
            print(f"Text content: {element.get_text()}")
            result = percentage_string_to_int(element.get_text())

            if (result > 95):
                print("Send notifcation")
                url = "https://api.telegram.org/bot6800893466:AAGwwvB358ZcLELioW_6cilYoV7YQ8oBkCc/sendMessage"
                params = {'chat_id': -847131721, 'text': f'Yii Here {result}'}
                response = send_get_request(url, params)
                if response and response.headers.get('Content-Type') == 'application/json; charset=utf-8':
                    json_data = response.json()
                    print("JSON Response Content:", json_data)
            

        else:
            print(f"No element found with ID '{element_id}'")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# Read URL and element ID from settings.json
settings = read_settings('settings.json')
url = settings.get('url')
element_id = settings.get('element_id')

# Validate settings
if not url or not element_id:
    print("URL or element ID is missing in the settings file.")
else:
    # Perform the search
    read_online_html_and_search_id(url, element_id)

