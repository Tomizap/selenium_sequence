import csv
import json
import os.path
from datetime import datetime
# import random
# import string

from colorama import Fore, Style

def creer_fichier_csv(data, filename):
    # Récupérer les clés de tous les dictionnaires pour définir les en-têtes
    en_tetes = data[0].keys()

    # Ouvrir le fichier CSV en mode écriture
    with open(filename, mode='w', newline='', encoding='utf-8') as fichier_csv:
        # Créer un objet DictWriter pour écrire les données
        writer = csv.writer(fichier_csv)

        # Écrire les en-têtes dans le fichier CSV
        writer.writerow(en_tetes)

        # Écrire les données à partir de la liste de dictionnaires
        for dictionnaire in data:
            writer.writerow(dictionnaire.values())


def add_data_to_csv(data=[], directory="C:/Users/Conta/Desktop/selenium_sequence/data", filename=None):
    print('add_data_to_csv')

    # Obtaining the current date
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")

    # Generate a unique filename if not provided
    if filename is None:
        filename = f"{date_string}_${filename}.csv"
        # filename = f"{date_string}_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '.csv'
    if '.csv' not in filename:
        filename = filename + ".csv"

    # Construct the full file path
    file_path = os.path.join(directory, filename)

    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    # Open the file in append mode if it exists, or write mode if it does not exist
    mode = 'a' if file_exists else 'w'

    # Extracting fieldnames from the first dictionary in the data list
    fieldnames = list(data[0].keys())

    # Create a set to store existing emails
    # existing_emails = set()

    # # If the file exists, read the existing data and populate the set of existing emails
    # if file_exists:
    #     with open(file_path, 'r') as file:
    #         reader = csv.DictReader(file)
    #         for row in reader:
    #             existing_emails.add(row['COMPANY_EMAIL'])       

    # # Filter the new data to exclude rows with existing emails
    # filtered_data = [row for row in data if row['COMPANY_EMAIL'] not in existing_emails]

    # Write the data to the file
    with open(file_path, mode, encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header if the file is newly created
        if mode == 'w':
            writer.writeheader()

        try:
            # Write the filtered data
            writer.writerows(data)
        except Exception as e:
            print(Fore.RED + f'error: {str(e)}')

        print(Fore.GREEN + f"The data has been successfully added to '{file_path}'.")
        print(Style.RESET_ALL)

# data_test = [{'COMPANY': {'APPLICATION_DIFFICULTY': '',
#              'APPLICATION_EXPERIENCE': '',
#              'APPLICATION_TIME': '',
#              'CREATION_DATE': '',
#              'EMAIL': '',
#              'EMPLOYEES_COUNT': '',
#              'JOBS_COUNT': '',
#              'LOCATION': '',
#              'NAME': '',
#              'PHONE': '',
#              'RATE': '',
#              'REVENUE': '',
#              'SECTOR': '',
#              'URL': '',
#              'WEBSITE': ''},
#  'EMAIL': '',
#  'LOCATION': '',
#  'NAME': '',
#  'PHONE': '',
#  'REVENUE': '',
#  'SPECIFICATION': '',
#  'TIME': '',
#  'URL': '',
#  'WEBSITE': '',
#  'WORTIME': ''}]

# # print(json.dump(data_test))

# add_data_to_csv(data_test, filename='test')