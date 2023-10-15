from pprint import pprint
import threading
import time

from selenium_sequence import *
# from selenium_sequence.main import Automnation
# from selenium_driver import SeleniumDriver
# from tzmongo import mongo


data = []
auth = []
headless = True

# driver = SeleniumDriver(headless=headless)

# ------------- INPUTS -------------

vente_idf = [
  # f'https://fr.indeed.com/emplois?q=commerce&l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=c90a7682c8c4da2e'
  # f'https://fr.indeed.com/emplois?q=vente&l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=6157b8933ab1c944&advn=4629412499192798'
]

medico_social_idf = [  
   f"https://www.google.com/maps/search/%C3%A9tablissement+d'accueil+m%C3%A9dicalis%C3%A9/@48.866726,2.3378585,12z/data=!3m1!4b1?entry=ttu",
  f"https://www.google.com/maps/search/foyer+d'accueil+m%C3%A9dicalis%C3%A9/@48.8665588,2.3378587,12z/data=!3m1!4b1?entry=ttu",
  f"https://www.google.com/maps/search/SESSAD/@48.8668931,2.3378582,12z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/Foyer+de+vie/@48.8663917,2.337859,12z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/institut+m%C3%A9dico-%C3%A9ducatif/@48.8670602,2.3378579,12z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/externat+m%C3%A9dico+psychologique/@48.8672274,2.3378576,12z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/EPHAD/@48.8672274,2.3378576,12z?entry=ttu",
   f"https://www.google.com/maps/search/Maison+d'enfants+%C3%A0+caract%C3%A8re+social/@48.8675616,2.337857,12z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/centre+d'accueil+de+jour/@48.8678959,2.3378565,12z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/unit%C3%A9s+d%E2%80%99enseignement+Autisme/@48.868063,2.3378562,12z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/cabinet+m%C3%A9dical/@48.8682302,2.3378559,12z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/centres+m%C3%A9dico-psycho-p%C3%A9dagogiques/@48.8682302,2.3378559,12z?entry=ttu",
   f"https://www.google.com/maps/search/ESAT/@48.8685644,2.3378553,12z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/Institut+th%C3%A9rapeutique+%C3%A9ducatif+et+p%C3%A9dagogique/@48.8685644,2.3378553,12z?entry=ttu",
   f"https://www.google.com/maps/search/maison+d%E2%80%99accueil%C2%A0sp%C3%A9cialis%C3%A9e/@48.8687316,2.3378551,12z?entry=ttu",

  f"https://www.google.com/maps/search/%C3%A9tablissement+d'accueil+m%C3%A9dicalis%C3%A9/@48.7706372,2.3841393,11.98z/data=!3m1!4b1?entry=ttu",
  f"https://www.google.com/maps/search/foyer+d'accueil+m%C3%A9dicalis%C3%A9/@48.7706372,2.3841393,11.98z/data=!3m1!4b1?entry=ttu",
  f"https://www.google.com/maps/search/SESSAD/@48.7706372,2.3841393,11.98z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/Foyer+de+vie/@48.7706372,2.3841393,11.98z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/institut+m%C3%A9dico-%C3%A9ducatif/@48.7706372,2.3841393,11.98z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/externat+m%C3%A9dico+psychologique/@48.7706372,2.3841393,11.98z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/EPHAD/@48.7706372,2.3841393,11.98z?entry=ttu",
   f"https://www.google.com/maps/search/Maison+d'enfants+%C3%A0+caract%C3%A8re+social/@48.7706372,2.3841393,11.98z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/centre+d'accueil+de+jour/@48.7706372,2.3841393,11.98z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/unit%C3%A9s+d%E2%80%99enseignement+Autisme/@48.7706372,2.3841393,11.98z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/cabinet+m%C3%A9dical/@48.7706372,2.3841393,11.98z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/centres+m%C3%A9dico-psycho-p%C3%A9dagogiques/@48.7706372,2.3841393,11.98z?entry=ttu",
   f"https://www.google.com/maps/search/ESAT/@48.7706372,2.3841393,11.98z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/Institut+th%C3%A9rapeutique+%C3%A9ducatif+et+p%C3%A9dagogique/@48.7706372,2.3841393,11.98z?entry=ttu",
   f"https://www.google.com/maps/search/maison+d%E2%80%99accueil%C2%A0sp%C3%A9cialis%C3%A9e/@48.7706372,2.3841393,11.98z?entry=ttu",

  f"https://www.google.com/maps/search/%C3%A9tablissement+d'accueil+m%C3%A9dicalis%C3%A9/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
  f"https://www.google.com/maps/search/foyer+d'accueil+m%C3%A9dicalis%C3%A9/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
  f"https://www.google.com/maps/search/SESSAD/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/Foyer+de+vie/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/institut+m%C3%A9dico-%C3%A9ducatif/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/externat+m%C3%A9dico+psychologique/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/EPHAD/@48.8690837,2.4955362,12.72z?entry=ttu",
   f"https://www.google.com/maps/search/Maison+d'enfants+%C3%A0+caract%C3%A8re+social/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/centre+d'accueil+de+jour/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/unit%C3%A9s+d%E2%80%99enseignement+Autisme/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/cabinet+m%C3%A9dical/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/centres+m%C3%A9dico-psycho-p%C3%A9dagogiques/@48.8690837,2.4955362,12.72z?entry=ttu",
   f"https://www.google.com/maps/search/ESAT/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
   f"https://www.google.com/maps/search/Institut+th%C3%A9rapeutique+%C3%A9ducatif+et+p%C3%A9dagogique/@48.8690837,2.4955362,12.72z?entry=ttu",
   f"https://www.google.com/maps/search/maison+d%E2%80%99accueil%C2%A0sp%C3%A9cialis%C3%A9e/@48.8690837,2.4955362,12.72z?entry=ttu",
]

sport_idf = [
  # f"https://www.google.com/maps/search/coach+sportif/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
  # f"https://www.google.com/maps/search/salle+de+sport/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
  f"https://www.google.com/maps/search/salle+de+fitness/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu",
  f"https://www.google.com/maps/search/salle+de+musculation/@48.8690837,2.4955362,12.72z/data=!3m1!4b1?entry=ttu"
]

secretaire_medical_idf = [
  #  f"https://fr.indeed.com/emplois?q=secr%C3%A9taire+m%C3%A9dical&l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=3c64d91c1a5776c8",
  #  f"https://candidat.pole-emploi.fr/offres/recherche?lieux=11R&motsCles=secr%C3%A9taire+m%C3%A9dical&natureOffre=E2&offresPartenaires=true&range=0-19&rayon=10&tri=0",
   f"https://www.hellowork.com/fr-fr/emploi/recherche.html?k=Secr%C3%A9taire+m%C3%A9dical&k_autocomplete=http%3A%2F%2Fwww.rj.com%2FCommun%2FPost%2FSecretaire_medical&l=%C3%8Ele-de-France&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fregion%2F11&ray=50&d=all&c=Alternance&p=1"
]

# ------------- THREADING -------------

automnation = Automnation(
  # urls=medico_social_idf, 
  # filename=filename,
  # auth=auth,
  _id='64f91b86bd602b8bd6d2ea76',
  headless=headless)
automnation.play()

# -------------- RESULT --------------

# automnation.play()
# data = automnation.data
# pprint(data)

time.sleep(20)
