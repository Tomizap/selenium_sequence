import time
import re

from colorama import Fore
import requests
from selenium.webdriver.common.keys import Keys
from selenium_driver import SeleniumDriver


class Finder:
    def __init__(self, driver=None, name=None, location=None) -> None:
        print(Fore.WHITE + 'Finder')
        self.driver = driver if driver is not None else SeleniumDriver()
        self.name = name if name is not None else ""
        self.location = location if location is not None else ""
        # self.google_query = f'{self.name} "@" "contact"'

    # -------------- GLOBAL -------------------

    def email(self) -> str:
        if self.location is None or self.name is None:
            return ''
        # print('email')
        regex_exp = r'[\w.+-]+@[\w-]+\.[\w.-]+'
        text = self.driver.find_element("body").get_property('innerText')
        regex = re.findall(regex_exp, text)
        if bool(regex):
            print(Fore.GREEN + f'email found: {regex[0]}')
            return regex[0]

        mail = self.google_search(regex_exp=regex_exp)
        if mail != '':
            print(Fore.WHITE + f'email found: {mail}')
            return mail
        
        # mail = self.google_api(regex_exp=regex_exp)
        # if mail != '':
        #     print(Fore.WHITE + 'email found: ' + mail)
        #     return mail

        print(Fore.RED + 'Unable de get email')
        print(Fore.WHITE)
        return ''

    def phone(self) -> str:
        if self.location is None or self.name is None:
            return ''
        # print(Fore.WHITE + 'phone')
        regex_exp = r'((\+33|0)[1-9](?:[\s.-]?[0-9]{2}){4})'
        
        text = self.driver.find_element("body").get_property('innerText')
        regex = re.findall(regex_exp, text)
        if bool(regex):
            print(Fore.GREEN + 'find phone')
            print(Fore.WHITE)
            return regex[0]
        
        phone = self.google_search(regex_exp=regex_exp)
        if phone != '':
            print(Fore.WHITE + f'phone found: {phone}')
            return str(phone).split("'")[1].replace(r'[\s.-]', '')

        # phone = self.pagejaunes(regex_exp=regex_exp)
        # if phone != '':
        #     print(Fore.WHITE + 'email found: ' + phone)
        #     return str(phone).split("'")[1].replace(r'[\s.-]', '')

        # # mail = self.google_api(regex_exp=regex_exp)
        # # if mail != '':
        # #     return str(mail).split("'")[1].replace(r'[\s.-]', '')

        print(Fore.RED + 'Unable de get phone')
        print(Fore.WHITE)
        return ''

    # def website(self) -> str:
    #     if self.location is None or self.name is None:
    #         return ''
        
    #     # print(Fore.WHITE + 'website')
    #     regex_exp = r'((\+33|0)[1-9](?:[\s.-]?[0-9]{2}){4})'
        
    #     text = self.driver.find_element("body").get_property('innerText')
    #     regex = re.findall(regex_exp, text)
    #     if bool(regex):
    #         print(Fore.GREEN + 'find website')
    #         print(Fore.WHITE)
    #         return regex[0]
        
    #     website = self.google_search(regex_exp=regex_exp)
    #     if website != '':
    #         print(Fore.WHITE + f'website found: {website}')
    #         return str(website).split("'")[1].replace(r'[\s.-]', '')

    #     print(Fore.RED + 'Unable de get website')
    #     print(Fore.WHITE)
    #     return ''

    # -------------- EXTERNAL -------------------

    def google_search(self, regex_exp=None) -> str:
        if self.location is None or self.name is None:
            return ''
        print(Fore.WHITE + 'google_search')

        self.driver.get(
            f'https://www.google.com/search?q={self.name} {self.location} contact')
        time.sleep(2)

        reg = re.findall(regex_exp, self.driver.find_element(
            'body').get_property('innerText'))
        if bool(reg) is True:
            # driver.close()
            return reg[0]
        
        print(Fore.RED + 'Unable to find google search')
        print(Fore.WHITE)
        return ''



# finder = Finder(name='luminess', location="paris")
# phone = finder.phone()
# print(phone)
# email = finder.email()
# print(email)
