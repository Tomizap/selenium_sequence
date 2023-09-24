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

# url = f"https://www.linkedin.com/jobs/search/?f_F=sale%2Cbd%2Ccust%2Ccnsl&f_I=27%2C19%2C143%2C31&f_T=506%2C165%2C535%2C1443%2C1192%2C22471%2C3265%2C381%2C5441&geoId=104246759&location=%C3%8Ele-de-France%2C%20France&refresh=true&sortBy=R"
# url = f"https://www.linkedin.com/jobs/search/?position=1&pageNum=0"
# URL OK
# url = f"https://candidat.pole-emploi.fr/offres/recherche?domaine=D&lieux=11R&natureOffre=E2&offresPartenaires=true&range=0-19&rayon=10&tri=0"
# url = f"https://www.hellowork.com/fr-fr/emploi/recherche.html?l=%C3%8Ele-de-France&d=all&c=Alternance&f=Commercial_technico_com&f=Commercial_particulier&f=Commercial_professionnel&f=Commercial_vendeur&f=Import_export_inter&f=Dir_management_resp&f=Negociation_gest_immo"
# url = f"https://fr.indeed.com/emplois?l=%C3%8Ele-de-France&sc=0kf%3Acmpsec%2848BZP%29jt%28apprenticeship%29%3B&vjk=3a5bbf0ed2a7e33c"
# url = f"https://emploi.lefigaro.fr/recherche/offres-emploi?q=cT12ZW50ZSZsb2NhdGlvbkxhYmVsPcOObGUtZGUtRnJhbmNlJmNvbnRyYWN0cz02JnJlZ2lvbj1GUi1JREY%3D"

urls = [
  # f"https://candidat.pole-emploi.fr/offres/recherche?domaine=D&lieux=11R&natureOffre=E2&offresPartenaires=true&range=0-19&rayon=10&tri=0",
  # f"https://candidat.pole-emploi.fr/offres/recherche?lieux=11R&natureOffre=FS,E2&offresPartenaires=true&range=0-19&rayon=10&tri=0",

  # f"https://www.hellowork.com/fr-fr/emploi/recherche.html?l=%C3%8Ele-de-France&d=all&c=Alternance&f=Commercial_technico_com&f=Commercial_particulier&f=Commercial_professionnel&f=Commercial_vendeur&f=Import_export_inter&f=Dir_management_resp&f=Negociation_gest_immo",
  f"https://www.hellowork.com/fr-fr/emploi/recherche.html?l=%C3%8Ele-de-France&d=all&c=Alternance&p=1",

  # f"https://fr.indeed.com/emplois?l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=c8ef35e1ba412c36",
  # f"https://fr.indeed.com/emplois?l=%C3%8Ele-de-France&sc=0kf%3Acmpsec%2848BZP%29jt%28apprenticeship%29%3B&vjk=3a5bbf0ed2a7e33c",

  # f"https://emploi.lefigaro.fr/recherche/offres-emploi?q=cT12ZW50ZSZsb2NhdGlvbkxhYmVsPcOObGUtZGUtRnJhbmNlJmNvbnRyYWN0cz02JnJlZ2lvbj1GUi1JREY%3D"
]

filename = "alternance_idf"

sequenceid = "65058f69a2556d1dca881977"

auth = [
  {
    "name": "li_at",
    "value": "AQEDAS3LRfIFvMDgAAABidzWa6AAAAGKkxVDMU4AkInBKbL9SNrI3HLUeGw0YVlfh0oM4uSd-svxX7RIwGk7oi8mLr7m7ZauqntilMJOhVn17TbA-Xbyj1UyZZcriEkY3Hk2UYhL54cuvzfd_dtsx6S_"
  }
]

threads = []

# d = mongo({
#   'db': "storage",
#   'collection': "tables"
# })
# pprint(d)

for url in urls:
  s = Sequence(
     url=url, 
     auth=auth, 
     filename=filename, 
     headless=headless,
     sequenceid=sequenceid)
  thread = threading.Thread(target=s.play)
  threads.append(thread)
  thread.start()
  time.sleep(2)

for thread in threads:
    thread.join()

# sequence = Sequence(url=urls[0], auth=auth, filename=filename, tableid=tableid)

# ----------------------------

# sequence.play()
# data = sequence.data
pprint(data)

time.sleep(9999)
