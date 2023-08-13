import csv
import os.path
from datetime import datetime
import random
import string

from colorama import Fore, Style


def add_data_to_csv(data, directory, filename=None):
    # Obtaining the current date
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")

    # Generate a unique filename if not provided
    if filename is None:
        filename = f"{date_string}_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '.csv'
    if '.csv' not in filename:
        filename = filename + ".csv"

    # Construct the full file path
    file_path = os.path.join(directory, filename)

    # Check if the file exists
    file_exists = os.path.isfile(file_path)
    print('file_exists: ' + str(file_exists))

    # Extracting fieldnames from the first dictionary in the data list
    fieldnames = list(data[0].keys())

    # Create a set to store existing emails
    existing_emails = set()

    # If the file exists, read the existing data and populate the set of existing emails
    if file_exists:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_emails.add(row['EMAIL'])

    # Filter the new data to exclude rows with existing emails
    filtered_data = [row for row in data if row['EMAIL'] not in existing_emails]

    # Append or create the file
    mode = 'a' if file_exists else 'w'
    print('mode: ' + str(file_exists))
    with open(file_path, mode, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header if the file is newly created
        if mode == 'w':
            writer.writeheader()

        # Write the filtered data
        writer.writerows(filtered_data)

    print(f"The data has been successfully added to '{file_path}'.")

    print(Fore.GREEN + f"The data has been successfully added to '{file_path}'.")
    print(Style.RESET_ALL)

# data_test = [{'ADDRESS': '1 place de la Mairie',
#   'CITY': 'Abbéville-la-Rivière',
#   'EMAIL': 'mairie-abbeville-la-riviere@wanadoo.fr',
#   'NAME': 'Mairie - Abbéville-la-Rivière',
#   'PHONE': '01 64 95 67 37',
#   'POSTCODE': '91150',
#   'URL': 'https://lannuaire.service-public.fr/navigation/ile-de-france/mairie'},
#  {'ADDRESS': 'Rue Gilles-de-Maupeou',
#   'CITY': 'Ableiges',
#   'EMAIL': 'mairie.ableiges95@wanadoo.fr',
#   'NAME': 'Mairie - Ableiges',
#   'PHONE': '01 34 66 01 12',
#   'POSTCODE': '95450',
#   'URL': 'https://lannuaire.service-public.fr/ile-de-france/essonne/8971767f-e50c-4d58-9e69-94e7a489f49a'},
#  {'ADDRESS': '8 rue de la Mairie',
#   'CITY': 'Ablis',
#   'EMAIL': 'mairie@ablis.fr',
#   'NAME': 'Mairie - Ablis',
#   'PHONE': '01 30 46 06 06',
#   'POSTCODE': '78660',
#   'URL': 'https://lannuaire.service-public.fr/ile-de-france/val-d-oise/55e63c96-f8a4-424c-a9fd-52ddf515b6ef'},
#  {'ADDRESS': '16 rue du Maréchal-Foch',
#   'CITY': 'Ablon-sur-Seine',
#   'EMAIL': '',
#   'NAME': 'Mairie - Ablon-sur-Seine',
#   'PHONE': '01 49 61 33 33',
#   'POSTCODE': '94480',
#   'URL': 'https://lannuaire.service-public.fr/ile-de-france/yvelines/c761b3fb-1ca7-4d30-bea4-6c81f7dd8030'},
#  {'ADDRESS': '12-14 boulevard Léon-Feix',
#   'CITY': 'Argenteuil',
#   'EMAIL': '',
#   'NAME': 'Mairie - Argenteuil',
#   'PHONE': '01 34 23 41 00',
#   'POSTCODE': '95100',
#   'URL': 'https://lannuaire.service-public.fr/ile-de-france/val-de-marne/c177c786-4474-436a-9aa7-1492d5c7627e'},
#  {'ADDRESS': "Place de l'Église",
#   'CITY': 'Argentières',
#   'EMAIL': 'mairie-argentieres77@wanadoo.fr',
#   'NAME': 'Mairie - Argentières',
#   'PHONE': '01 64 06 01 30',
#   'POSTCODE': '77390',
#   'URL': 'https://lannuaire.service-public.fr/ile-de-france/val-d-oise/5e27d725-abf2-4cc1-85fb-c7da1f2999c0'},
#  {'ADDRESS': '9 rue du Chef-de-Ville',
#   'CITY': 'Armentières-en-Brie',
#   'EMAIL': 'mairie.armentieresenbrie@orange.fr',
#   'NAME': 'Mairie - Armentières-en-Brie',
#   'PHONE': '01 64 35 51 99',
#   'POSTCODE': '77440',
#   'URL': 'https://lannuaire.service-public.fr/ile-de-france/seine-et-marne/4aca9232-ec73-4db2-8adf-c67fb26faf2c'},
#  {'ADDRESS': '15-17 rue Robert-Schuman',
#   'CITY': 'Arnouville',
#   'EMAIL': 'sgeneral@arnouville95.org',
#   'NAME': 'Mairie - Arnouville',
#   'PHONE': '01 30 11 16 16',
#   'POSTCODE': '95400',
#   'URL': 'https://lannuaire.service-public.fr/ile-de-france/seine-et-marne/88f0cd29-0b15-45fd-b698-9c58a23f2a7a'},
#  {'ADDRESS': "8 place de l'Église",
#   'CITY': 'Arnouville-les-Mantes',
#   'EMAIL': 'mairie.arnouville.les.mantes@wanadoo.fr',
#   'NAME': 'Mairie - Arnouville-les-Mantes',
#   'PHONE': '01 30 42 60 17',
#   'POSTCODE': '78790',
#   'URL': 'https://lannuaire.service-public.fr/ile-de-france/val-d-oise/36d78a20-3e71-483e-a07c-9a57593e3b2d'}]


# add_data_to_csv(data_test, "D:/PythonPackages/selenium_scrapper/scrapping/", "2023-07-15_mairies-idf")