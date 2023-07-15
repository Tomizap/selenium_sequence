from pprint import pprint
import time

from selenium_sequence import Sequence
from selenium_driver import SeleniumDriver
data = []

# --- TESTING ZONE ---

driver = SeleniumDriver()
config = {
    "user": {
        "email": "zaptom.pro@gmail.com",
        "password": "Tom01032000",
        "phone": "066577418"
    },
}
while not driver.is_attached('body > .application-outlet *'):
    driver.get('https://linkedin.com')
    if driver.is_attached('#session_key'):
        driver.write('#session_key', config['user']['email'])
        driver.write('#session_password', config['user']['password'])
        driver.click('[data-id="sign-in-form__footer"] button')
        time.sleep(3)
    time.sleep(2)
    driver.captcha()
print('logged in !')

url = f"https://www.linkedin.com/search/results/people/?geoUrn=%5B%22104246759%22%5D&keywords=recruteur&origin=FACETED_SEARCH&profileLanguage=%5B%22fr%22%5D&searchId=10ec62bf-5513-4071-a529-74b7cacc79a9&sid=Tj-"
filename = "2023-07-15_recruiters-idf"

# --- END TESTING ZONE ---

sequence = Sequence(url=url, filename=filename, data=data, driver=driver)
sequence.play()
data = sequence.data
pprint(data)

time.sleep(9999)
