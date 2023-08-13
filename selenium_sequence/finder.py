import time
import re

from colorama import Fore
import requests
from selenium.webdriver.common.keys import Keys
from selenium_driver import SeleniumDriver


class Finder:
    def __init__(self, driver=None, name=None, location=None, title=None) -> None:
        print(Fore.WHITE + 'Finder')
        self.driver = driver
        self.name = name
        self.location = location
        self.title = title
        self.google_query = f'{self.name} "@" "contact"'

    # -------------- ON PAGE -------------------

    def email(self) -> str:
        print('email')
        regex_exp = r'[\w.+-]+@[\w-]+\.[\w.-]+'
        # time.sleep(2)
        text = self.driver.find_element("body").get_property('innerText')
        regex = re.findall(regex_exp, text)
        if bool(regex):
            return regex[0]
        else:
            print(Fore.RED + 'Unable de get email')
            print(Fore.WHITE)
            return ''
        # mail = self.google_search(regex_exp=regex_exp)
        # if mail != '':
        #     print(Fore.WHITE + 'email found: ' + mail)
        #     return mail
        # mail = self.google_api(regex_exp=regex_exp)
        # if mail != '':
        #     print(Fore.WHITE + 'email found: ' + mail)
        #     return mail
        # print(Fore.RED + 'Unable de get email')
        # return ''

    def phone(self) -> str:
        print(Fore.WHITE + 'phone')
        regex_exp = r'((\+33|0)[1-9](?:[\s.-]?[0-9]{2}){4})'
        # time.sleep(2)
        text = self.driver.find_element("body").get_property('innerText')
        # print(text)
        regex = re.findall(regex_exp, text)
        if bool(regex):
            return regex[0]
        else:
            print(Fore.RED + 'Unable de get phone')
            print(Fore.WHITE)
            return ''
        # phone = self.google_search(regex_exp=regex_exp)
        # if phone != '':
        #     print(Fore.WHITE + 'email found: ' + phone)
        #     return str(phone).split("'")[1].replace(r'[\s.-]', '')
        # phone = self.pagejaunes(regex_exp=regex_exp)
        # if phone != '':
        #     print(Fore.WHITE + 'email found: ' + phone)
        #     return str(phone).split("'")[1].replace(r'[\s.-]', '')
        # # mail = self.google_api(regex_exp=regex_exp)
        # # if mail != '':
        # #     return str(mail).split("'")[1].replace(r'[\s.-]', '')
        # print(Fore.RED + 'Unable de get email')
        # return ''

    # -------------- EXTERNAL -------------------

    def google_search(self, regex_exp=None) -> str:
        if self.location is None or self.name is None:
            return ''
        print(Fore.WHITE + 'google_search')
        driver = SeleniumDriver(inconito=True)

        driver.get(
            f'https://www.google.com/search?q={self.name + " " + self.location}&oq=ds&gs_lcrp'
            f'=EgZjaHJvbWUyBggAEEUYOTIHCAEQABiPAjIHCAIQABiPAjIHCAMQABiPAtIBBzQ0NmowajSoAgCwAgA&sourceid=chrome&ie=UTF'
            f'-8')
        time.sleep(2)
        reg = re.findall(regex_exp, driver.find_element(
            'body').get_property('innerText'))
        if bool(reg):
            # driver.close()
            return reg[0]

        driver.write('[name=q]', self.google_query)
        driver.click('button.Tg7LZd')
        time.sleep(2)
        driver.write('[name=q]', self.google_query)
        driver.write('[name=q]', Keys.ENTER)
        time.sleep(2)
        reg = re.findall(regex_exp, driver.find_element(
            'body').get_property('innerText'))
        if bool(reg):
            # driver.close()
            return reg[0]

        driver.write('[name=q]', self.name)
        driver.click('button.Tg7LZd')
        time.sleep(2)
        driver.write('[name=q]', self.name)
        driver.write('[name=q]', Keys.ENTER)
        time.sleep(2)
        reg = re.findall(regex_exp, driver.find_element(
            'body').get_property('innerText'))
        if bool(reg):
            # driver.close()
            return reg[0]

        # driver.close()
        print(Fore.RED + 'Unable de find search')
        return ''

    def google_api(self, regex_exp=None) -> str:
        if self.location is None or self.name is None:
            return ''
        print(Fore.WHITE + 'google_api')
        params = {
            "q": self.google_query,
            "key": "AIzaSyDS38fo7o75VyF_6LseOhYu-okEKdm5PZs",
            "cx": "e286732fc0ec94b78"
        }
        response = requests.get(
            "https://customsearch.googleapis.com/customsearch/v1", params=params)
        regex = re.findall(regex_exp, str(response.json()))
        if response.status_code == 200:
            if bool(regex):
                # print(Fore.WHITE + str(regex[0]))
                return regex[0]
            else:
                print(Fore.RED + 'Unable to find regex')
                return ''
        else:
            print(Fore.RED + 'Unable to get google api')
            return ''

    def pagejaunes(self, regex_exp=None) -> str:
        if self.location is None or self.name is None or self.title is None:
            return ''
        print(Fore.WHITE + 'pagejaunes')
        driver = SeleniumDriver(inconito=True)
        # url = f"https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui={self.name}&ou={
        # self.location}&univers=pagesjaunes&idOu="
        driver.get("https://www.pagesjaunes.fr/annuaire/chercherlespros")
        time.sleep(5)
        driver.click("#didomi-notice-agree-button")
        print(self.name)

        driver.write('input#quoiqui', self.name)
        driver.write('input#ou', self.location)
        driver.click('#form_motor_pagesjaunes button[type="submit"]')
        time.sleep(4)
        driver.click("#listResults li > div > button")
        time.sleep(1)
        text = driver.find_element("body").get_property('innerHTML')
        print(text)
        regex = re.findall(regex_exp, text)
        driver.close()
        if bool(regex):
            return regex[0]
        print(Fore.RED + "unable to find regex")
        return ''



# finder = Finder(name='luminess', location="paris")
# phone = finder.phone()
# print(phone)
