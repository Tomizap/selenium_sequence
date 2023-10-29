import time
import re

from colorama import Fore, Style
import requests
from selenium.webdriver.common.keys import Keys
from selenium_driver import SeleniumDriver


class Finder:
    def __init__(self, driver=None, name=None, location=None) -> None:
        print(Fore.WHITE + 'Finder')

        self.driver = SeleniumDriver()
        self.name = name if name is not None else ""
        self.location = location if location is not None else ""

    def clear_phone(self, phone):
        phone = str(phone)
        if "'" in phone:
            phone = phone.split("'")[1]
        phone = phone.replace(r'[\s\.\-]', '')
        return phone
    
    def close(self):
        self.driver.close()

    # -------------- GLOBAL -------------------

    def email(self) -> str:
        if self.location is None or self.location == "" or self.name is None or self.name == '':
            return ''
        # print('email')
        regex_exp = r'[\w.+-]+@[\w-]+\.[\w.-]+'
        text = self.driver.find_element("body").get_property('innerText')
        regex = re.findall(regex_exp, text)
        if bool(regex):
            print(Fore.GREEN + f'email found: {regex[0]}')
            return regex[0]

        mail = self.google_search(q=f"{self.name} {self.location} contact email", regex_exp=regex_exp)
        if mail != '':
            print(Fore.GREEN + f'email found: {mail}')
            return mail

        print(Fore.RED + 'Unable de get email')
        print(Style.RESET_ALL)
        return ''

    def phone(self) -> str:
        if self.location is None or self.location == "" or self.name is None or self.name == '':
            return ''
        regex_exp = r'((\+33|0)[1-9](?:[\s.-]?[0-9]{2}){4})'
        
        text = self.driver.find_element("body").get_property('innerText')
        regex = re.findall(regex_exp, text)
        if bool(regex):
            phone = self.clear_phone(regex[0])
            print(Fore.GREEN + f'phone found: {phone}')
            return phone
            
        
        phone = self.google_search(q=f"{self.name} {self.location} contact phone", regex_exp=regex_exp)
        if phone != '':
            phone = self.clear_phone(phone)
            print(Fore.GREEN + f'phone found: {phone}')
            return phone

        print(Fore.RED + 'Unable de get phone')
        print(Style.RESET_ALL)
        return ''
    
    def website(self) -> str:
        # self.driver.get('')
        # if self.name is None or self.name == '':
        #     return ''
        w = self.google_search(
            q=f"intext:{self.name}",
            css_selector='#rso a')
        if w == "":
            print(Fore.RED + 'Unable to find google search')
            print(Style.RESET_ALL)
        self.w = w
        return w
    
    def indeed(self, regex_url=[
        "indeed.com/cmp/",
    ], prefix="") -> str:
        # if self.name is None or self.name == '':
        #     return ''
        url = self.google_search(
            q=f"{prefix} {self.name} @indeed",
            # regex_exp=r'indeed\.com\/cmp\/',
            css_selector='#rso a')
        for regex in regex_url:
            if regex in url:
                return url
        print(Fore.RED + 'Unable to find indeed')
        print(Style.RESET_ALL)
        return ''
        
    def linkedin(self, regex_url=[
        "linkedin.com/company/",
        "linkedin.com/shool/"
    ], prefix="") -> str:
        url = self.google_search(
            q=f"{prefix} {self.name} @linkedin",
            # regex_exp=r'linkedin\.com\/company\/',
            css_selector='#rso a')
        for regex in regex_url:
            if regex in url:
                return url
        print(Fore.RED + 'Unable to find linkedin')
        print(Style.RESET_ALL)
        return ''
    
    def facebook(self, regex_url=[
        "facebook.com/"
    ], prefix="") -> str: 
        url = self.google_search(
            q=f"{prefix} {self.name} @facebook",
            # regex_exp=r'facebook\.com/',
            css_selector='#rso a')
        for regex in regex_url:
            if regex in url:
                return url
        print(Fore.RED + 'Unable to find facebook')
        print(Style.RESET_ALL)
        return ''
    
    def youtube(self, regex_url=[
        "youtube.com/@"
    ], prefix="channel") -> str: 
        url = self.google_search(
            q=f"{prefix} {self.name} @facebook",
            # regex_exp=r'facebook\.com/',
            css_selector='#rso a')
        for regex in regex_url:
            if regex in url:
                return url
        print(Fore.RED + 'Unable to find youtube')
        print(Style.RESET_ALL)
        return ''
    
    def instagram(self, regex_url=[
        r"instagram.com\/[\w.]+\/\?hl="
    ], prefix="channel") -> str: 
        url = self.google_search(
            q=f"{prefix} {self.name} @facebook",
            # regex_exp=r'facebook\.com/',
            css_selector='#rso a')
        for regex in regex_url:
            if regex in url or bool(re.search(regex, url)):
                return url
        print(Fore.RED + 'Unable to find instagram')
        print(Style.RESET_ALL)
        return ''
        
    # def linkedin(self) -> str:
    #     return ''
        
    # def account_instagram(self) -> str:
    #     url = self.google_search(
    #         q=f"{self.name} @instagram",
    #         # regex_exp=r'facebook\.com/',
    #         css_selector='#rso a')
    #     return url if "instagram.com/" in url else ""

    # -------------- EXTERNAL -------------------

    def google_search(self, q="", regex_exp=None, css_selector=None) -> str:
        if self.name is None or self.name == '':
            return ''
        print(Fore.WHITE + 'google_search')

        self.driver.get(f'https://www.google.com/search?q={q}')
        # time.sleep(2)

        if regex_exp is not None:
            reg = re.findall(regex_exp, self.driver.find_element(
                'body').get_property('innerText'))
            if bool(reg) is True:
                # driver.close()
                return reg[0]
            
        if css_selector is not None:
            try:
                element = self.driver.find_element(css_selector)
                return element.get_property('href')
            except:
                pass
        
        print(Fore.RED + 'Unable to find google search')
        print(Style.RESET_ALL)
        return ''


# finder = Finder(name='luminess', location="paris")
# phone = finder.phone()
# print(phone)
# email = finder.email()
# print(email)
