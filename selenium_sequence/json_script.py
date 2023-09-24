import os
import json
from datetime import datetime

from colorama import Fore, Style

def add_data_to_json(data=[], directory="D:/CODE/python/packages/selenium_sequence/data", filename=None):
    # Obtaining the current date
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")

    # Generate a unique filename if not provided
    if filename is None:
        filename = f"{date_string}_${filename}.json"
        # filename = f"{date_string}_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '.json'
    if '.json' not in filename:
        filename = filename + ".json"

    # Construct the full file path
    file_path = os.path.join(directory, filename)

    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    # If the file exists, load existing data
    existing_data = []
    if file_exists:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)

    # Extracting keys from the first dictionary in the data list
    keys = list(data[0].keys())

    # Create a set to store existing emails
    # existing_emails = set()

    # # If the file exists, populate the set of existing emails
    # for entry in existing_data:
    #     try:
    #         if entry['COMPANY_EMAIL'] is not None and entry['COMPANY_EMAIL'] != '':
    #             existing_emails.add(entry['COMPANY_EMAIL'])
    #     except:
    #         pass

    # # Filter the new data to exclude entries with existing emails
    # filtered_data = [entry for entry in data if entry['COMPANY_EMAIL'] is None or entry['COMPANY_EMAIL'] != "" or entry['COMPANY_EMAIL'] not in existing_emails]

    # Add the filtered data to the existing data
    existing_data.extend(data)
    # existing_data.extend(filtered_data)

    # Write the data to the file
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

    print(Fore.GREEN + f"The data has been successfully added to '{file_path}' as JSON.")
    print(Style.RESET_ALL)

# Example usage:
# data = [{'COMPANY_EMAIL': 'email1@example.com', 'other_field': 'value1'},
#         {'COMPANY_EMAIL': 'email2@example.com', 'other_field': 'value2'},
#         {'COMPANY_EMAIL': 'email3@example.com', 'other_field': 'value3'}]

# add_data_to_json(data, './data_directory', 'data.json')
