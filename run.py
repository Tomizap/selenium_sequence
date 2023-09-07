from pprint import pprint
import time

from selenium_sequence import Sequence
from selenium_driver import SeleniumDriver


data = []
driver = SeleniumDriver()
config = {
  "_id": "",
  "urls" : ["https://www.linkedin.com/jobs/search/?currentJobId=3671928543&geoId=105015875&keywords=rh&location=France&refresh=true"],
  "user": {
      "email": "reinofabrice@gmail.com",
      "password": "Paris75017",
  },
  "setting": {
      "excluded_keywords": [],
      "excluded_companies": ['iscod', 'aston'],
      "infinite": True,
      "scrap": False,
      "presets": {
          "phone": "066577418",
          "name": "tom",
          "nom": "tom",
          "pays": "fr",
          "mail": "zaptom.pro@gmail.com",
          "linkedin": "https://www.linkedin.com/in/tom-zapico/",
      }
  }
}

# ------------- LINKEDIN TESTING ZONE -------------

# while not driver.is_attached('body > .application-outlet *'):
#     driver.get('https://linkedin.com')
#     if driver.is_attached('#session_key'):
#         driver.write('#session_key', config['user']['email'])
#         driver.write('#session_password', config['user']['password'])
#         driver.click('[data-id="sign-in-form__footer"] button')
#         time.sleep(3)
#     time.sleep(2)
#     driver.captcha()
# print('logged in !')

# ------------- INDEED TESTING ZONE -------------

# email_ok = False
# password_ok = False
# while not driver.is_attached('#container > #app-root *'):
#   driver.get('https://secure.indeed.com')
#   time.sleep(7)
#   # EMAIL
#   if driver.is_attached('#emailform'):
#     driver.write('#emailform input', config["user"]['email'])
#     driver.click('#emailform button')
#     if driver.is_attached('#emailform'):
#         driver.write('#emailform input', config["user"]['email'])
#   time.sleep(3)
#   driver.click('#onetrust-accept-btn-handler')
#   driver.click('#auth-page-google-password-fallback')
#   # while not driver.is_attached('#loginform'):
#   #     time.sleep(1)
#   # PASSWORD
#   time.sleep(3)
#   driver.write('#loginform input[type="password"]',
#                     config["user"]['password'])
#   driver.click('#auth-page + button')
#   if driver.is_attached('#loginform'):
#       driver.write('#loginform input[type="password"]',
#                         config["user"]['password'])
#       driver.click('#auth-page + button')
#   # PHONE
#   time.sleep(3)
#   if driver.is_attached('#two-factor-auth-form'):
#     while driver.is_attached('#two-factor-auth-form'):
#       time.sleep(1)
#   time.sleep(3)
#   if not driver.is_attached('#container > #app-root > *'):
#     time.sleep(10)
# print('logged in !')

url = f"https://fr.indeed.com/emplois?q=commercial&l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=0f10ac230ee08eb2"
filename = "testing"

sequence = Sequence(url=url, filename=filename)
sequence.play()

# filename = "school-idf"

# url = f"https://www.123ecoles.com/etablissements-scolaires-a-paris-75"
# sequence = Sequence(url=url, filename=filename, data=data, driver=driver)
# sequence.play()
# url = f"https://www.123ecoles.com/etablissements-scolaires-essonne-91"
# sequence = Sequence(url=url, filename=filename, data=data, driver=driver)
# sequence.play()
# url = f"https://www.123ecoles.com/etablissements-scolaires-hauts-de-seine-92"
# sequence = Sequence(url=url, filename=filename, data=data, driver=driver)
# sequence.play()
# url = f"https://www.123ecoles.com/etablissements-scolaires-seine-et-marne-77"
# sequence = Sequence(url=url, filename=filename, data=data, driver=driver)
# sequence.play()
# url = f"https://www.123ecoles.com/etablissements-scolaires-val-de-marne-94"
# sequence = Sequence(url=url, filename=filename, data=data, driver=driver)
# sequence.play()
# url = f"https://www.123ecoles.com/etablissements-scolaires-val-doise-95"
# sequence = Sequence(url=url, filename=filename, data=data, driver=driver)
# sequence.play()
# url = f"https://www.123ecoles.com/etablissements-scolaires-yvelines-78"
# sequence = Sequence(url=url, filename=filename, data=data, driver=driver)
# sequence.play()

# sequence = Sequence(driver=driver, sequence={
#     ":loop": {
#         "pagination": 1,
#         # "pagination": 'div.jobs-search-results-list__pagination li:last-child',
#         "listing": {
#             ":execute_script": 'document.querySelector("div.jobs-search-results-list").scroll(0, 999999)',
#             ":get:all": {"property": "href",
#                         "selector": 'div.artdeco-entity-lockup__title > a.job-card-container__link'},
#             ":click": 'div.jobs-search-results-list__pagination li.selected + li',
#         },
#     }
# })
# sequence.play()
# print(sequence.data)

# -------------- END TESTING ZONE --------------

# data = sequence.data
# pprint(data)

time.sleep(9999)
