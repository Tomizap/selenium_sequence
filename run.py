from selenium_sequence import *

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

job_marketing_urls = [
  f"https://fr.indeed.com/emplois?q=marketing&l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=574f5dd76d57c018",
  f"https://candidat.pole-emploi.fr/offres/recherche?lieux=11R&motsCles=marketing&natureOffre=E2&offresPartenaires=true&range=0-19&rayon=10&tri=0",
  f"https://www.hellowork.com/fr-fr/emploi/recherche.html?k=marketing&l=%C3%8Ele-de-France&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fregion%2F11&c=Alternance&p=1",
  # f"https://www.welcometothejungle.com/fr/jobs?refinementList%5Boffices.country_code%5D%5B%5D=FR&refinementList%5Bcontract_type%5D%5B%5D=APPRENTICESHIP&query=marketing&page=1"
]

sport_idf = [
  f"https://www.google.com/maps/search/coach+sportif/@@48.9958471,2.5505606,10.49z?entry=ttu",
  f"https://www.google.com/maps/search/salle+de+sport/@@48.9958471,2.5505606,10.49z?entry=ttu",
  f"https://www.google.com/maps/search/salle+de+fitness/@@48.9958471,2.5505606,10.49z?entry=ttu",
  f"https://www.google.com/maps/search/salle+de+musculation/@@48.9958471,2.5505606,10.49z?entry=ttu",
  f"https://www.google.com/maps/search/coach+priv%C3%A9/@@48.9958471,2.5505606,10.49z?entry=ttu",
]

secretaire_medical_idf = [
  #  f"https://fr.indeed.com/emplois?q=secr%C3%A9taire+m%C3%A9dical&l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=3c64d91c1a5776c8",
   f"https://candidat.pole-emploi.fr/offres/recherche?lieux=11R&motsCles=secr%C3%A9taire+m%C3%A9dical&natureOffre=E2&offresPartenaires=true&range=0-19&rayon=10&tri=0",
  #  f"https://www.hellowork.com/fr-fr/emploi/recherche.html?k=Secr%C3%A9taire+m%C3%A9dical&k_autocomplete=http%3A%2F%2Fwww.rj.com%2FCommun%2FPost%2FSecretaire_medical&l=%C3%8Ele-de-France&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fregion%2F11&ray=50&d=all&c=Alternance&p=1"
  # f"https://labonnealternance.apprentissage.beta.gouv.fr/recherche-apprentissage?&display=list&job_name=Secr%C3%A9tariat%20m%C3%A9dical&romes=J1303,M1609,M1607&radius=60&lat=48.784506&lon=2.452976&zipcode=94000&insee=94028&address=Cr%C3%A9teil%2094000&s=1697759569890"
]

ecole_com_idf = [
  # f'https://labonnealternance.apprentissage.beta.gouv.fr/recherche-apprentissage?&display=list&job_name=Administratif%2C%20secr%C3%A9tariat%2C%20assistanat&romes=M1701,M1605,M1608,M1607,M1601,M1602,M1606,M1604&radius=30&lat=48.859&lon=2.347&zipcode=75001&insee=75056&address=Paris&s=1698046308063',
  # f'https://labonnealternance.apprentissage.beta.gouv.fr/recherche-apprentissage?&display=list&job_name=Marketing%2C%20vente&romes=M1707,M1703,E1401,M1705,E1103&radius=30&lat=48.859&lon=2.347&zipcode=75001&insee=75056&address=Paris&s=1698046075114',
  # f'https://labonnealternance.apprentissage.beta.gouv.fr/recherche-apprentissage?&display=list&job_name=Management%20commercial%20operationnel&romes=D1501,D1506,M1704,M1705,D1401&radius=30&lat=48.859&lon=2.347&zipcode=75001&insee=75056&address=Paris&s=1698046029970',
  f'https://labonnealternance.apprentissage.beta.gouv.fr/recherche-apprentissage?&display=list&job_name=Negociation%20et%20digitalisation%20de%20la%20relation%20client&romes=D1406,M1703,D1501,M1704,D1401&radius=60&lat=48.859&lon=2.347&zipcode=75001&insee=75056&address=Paris&s=1698045960192'
]

# ------------- RUNNING -------------

automnation = Automnation(
  urls=sport_idf, 
  # filename=filename,
  _id='6539887fe19d005aed6bd3df',
  headless=True)
automnation.play()
# print(automnation.data)
