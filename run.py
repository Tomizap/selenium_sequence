from pprint import pprint
import threading
import time

from selenium_sequence import Sequence
from selenium_driver import SeleniumDriver
# from tzmongo import mongo


data = []
auth = []
headless = False

# driver = SeleniumDriver(headless=headless)

# ------------- INPUTS -------------

urls = [
  # f'https://candidat.pole-emploi.fr/offres/recherche?lieux=11R&motsCles=secr%C3%A9taire+m%C3%A9dical&natureOffre=FS,E2&offresPartenaires=true&range=0-19&rayon=10&tri=0',
  # f"https://candidat.pole-emploi.fr/offres/recherche?lieux=11R&motsCles=moniteur+de+sport&natureOffre=FS,E2&offresPartenaires=true&range=0-19&rayon=10&tri=0",
  # f"https://candidat.pole-emploi.fr/offres/recherche?domaine=D&lieux=11R&natureOffre=E2&offresPartenaires=true&range=0-19&rayon=10&tri=0",
  # f"https://candidat.pole-emploi.fr/offres/recherche?lieux=11R&natureOffre=FS,E2&offresPartenaires=true&range=0-19&rayon=10&tri=0",

  # f"https://www.hellowork.com/fr-fr/emploi/recherche.html?k=Secr%C3%A9taire+m%C3%A9dical&k_autocomplete=http%3A%2F%2Fwww.rj.com%2FCommun%2FPost%2FSecretaire_medical&l=%C3%8Ele-de-France&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fregion%2F11&ray=20&c=Alternance&msa=&cod=all&d=all&c_idesegal=",
  # f"https://www.hellowork.com/fr-fr/emploi/recherche.html?k=Coach+sportif&k_autocomplete=http%3A%2F%2Fwww.rj.com%2FCommun%2FPost%2FEntraineur_sportif&l=%C3%8Ele-de-France&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fregion%2F11&ray=20&msa=&cod=all&d=all&c_idesegal=",
  # f"https://www.hellowork.com/fr-fr/emploi/recherche.html?l=%C3%8Ele-de-France&d=all&c=Alternance&f=Commercial_technico_com&f=Commercial_particulier&f=Commercial_professionnel&f=Commercial_vendeur&f=Import_export_inter&f=Dir_management_resp&f=Negociation_gest_immo",
  # f"https://www.hellowork.com/fr-fr/emploi/recherche.html?l=%C3%8Ele-de-France&d=all&c=Alternance&p=1",

  f"https://fr.indeed.com/emplois?q=secr%C3%A9taire+m%C3%A9dicale&l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=3c64d91c1a5776c8",
  # f"https://fr.indeed.com/emplois?q=coach+sportif&l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=cfb891998a9ab649",
  # f"https://fr.indeed.com/emplois?l=%C3%8Ele-de-France&sc=0kf%3Acmpsec%2848BZP%29jt%28apprenticeship%29%3B&vjk=3a5bbf0ed2a7e33c",
  # f"https://fr.indeed.com/emplois?l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=c8ef35e1ba412c36",

  # f"https://www.linkedin.com/jobs/search/?currentJobId=3709797901&f_F=sale%2Cbd%2Ccnsl%2Cgenb&f_JT=I&geoId=105015875&location=France&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R",
  # f"https://www.linkedin.com/jobs/search/?currentJobId=3718394552&f_JT=I&geoId=105015875&location=France&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R",

  # f"https://emploi.lefigaro.fr/recherche/offres-emploi?q=cT12ZW50ZSZsb2NhdGlvbkxhYmVsPcOObGUtZGUtRnJhbmNlJmNvbnRyYWN0cz02JnJlZ2lvbj1GUi1JREY%3D"

  # f"https://labonnealternance.apprentissage.beta.gouv.fr/recherche-apprentissage?&display=list&job_name=Secr%C3%A9tariat%20m%C3%A9dical&romes=J1303,M1609,M1607&radius=60&lat=48.859&lon=2.347&zipcode=75001&insee=75056&address=Paris&s=1696539441231",

  # f"https://www.onisep.fr/ressources/univers-formation/formations/Post-bac/bts-negociation-et-digitalisation-de-la-relation-client#etablissements",

  # f'https://www.google.com/maps/search/traiteur/@48.8285713,2.1879121,13z?entry=ttu'
]

# filename = "google_maps_test"

# auth = [
#   {
#     "name": "li_at",
#     "value": "AQEFARABAAAAAAyVP6AAAAGKzgCDYgAAAYryEQ6gTgAAs3VybjpsaTplbnRlcnByaXNlQXV0aFRva2VuOmVKeGpaQUFDTnYyZ1MyRDZmY0lrTUwweU9Jb1J4QkR4NHBrR1p2Qm1xMWN4c0FBQW5DVUd2UT09XnVybjpsaTplbnRlcnByaXNlUHJvZmlsZToodXJuOmxpOmVudGVycHJpc2VBY2NvdW50OjEwMzc2NDY5MCwxMTYzNTExMjIpXnVybjpsaTptZW1iZXI6NzY4Mjk2NDM0QDnUVXGPEt4rHLMMA2ACQscjmvp20_E_K9KuLW214hV42TI4F6qcdZeTBbLfS2gNDq6PDNCpxnrUEcJItQ33p2ZYb-sgAZM77qe2YG2WEHcseVB-51lejQvBRN09-RmBAyJWNKF2qsO1ijV8J-yMBygresG8YeTUq6hlRy-LdrgP4EroWZBBuCCPb4ZXx6hfEW5Ovw"
#   }
# ]

automnation_id = "64f91b86bd602b8bd6d2ea76"
filename = None

# threads = []

# d = mongo({
#   'db': "storage",
#   'collection': "tables"
# })
# pprint(d)

# for url in urls:
  # s = Sequence(
  #    urls=urls, 
  #    auth=auth, 
  #    filename=filename, 
  #    headless=headless,
  #    automnation={"_id": automnation_id})
  # thread = threading.Thread(target=s.play)
#   threads.append(thread)
#   thread.start()
#   time.sleep(2)

# for thread in threads:
#     thread.join()

sequence = Sequence(
  url=urls[0], 
  # auth=auth,
  headless=headless)

# ----------------------------

sequence.play()
# data = sequence.data
# pprint(data)

time.sleep(9999)
