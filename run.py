from pprint import pprint
import time

from selenium_sequence import Sequence
from selenium_driver import SeleniumDriver
data = []

# --- TESTING ZONE ---

driver = SeleniumDriver()

# config = {
#     "user": {
#         "email": "zaptom.pro@gmail.com",
#         "password": "Tom01032000",
#         "phone": "066577418"
#     },
# }
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

# url = f"https://www.linkedin.com/jobs/search/?currentJobId=3620288377&f_AL=true&f_JT=I&keywords=seo&location=Ile-de-France"
# filename = "testing"

# sequence = Sequence(url=url, filename=filename, data=data, driver=driver)
# sequence.play()

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

# sequence = Sequence(driver=self.driver, sequence={
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

# --- END TESTING ZONE ---

# data = sequence.data
# pprint(data)

time.sleep(9999)
