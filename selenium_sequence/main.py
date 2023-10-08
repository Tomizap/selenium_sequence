import re
import time
from pprint import pprint

from colorama import Fore, Style
from selenium_driver import SeleniumDriver
from tzmongo import mongo

from selenium_sequence.finder import Finder

from .models import find_model
from .data import get_element_data, get_elements_data
from .chrono import Chronos
from .csv_script import add_data_to_csv
from .json_script import add_data_to_json
from .items import *
from .tzprint import *


class Sequence:

    def __init__(
            self, 
            driver=None, 
            url=None, 
            item=None, 
            data=[], 
            sequence=None,
            depth=0,
            # step={}, 
            # auth=None, 
            headless=False,
            sequenceid=None,
            automnation={},
            filename=None) -> None:

        self.chrono = Chronos()
        self.chrono.start()

        self.depth = depth
        print(f'init Sequence (depth: {self.depth})', self.depth)

        # self.automnation = mongo({
        #     "selector": {automnation.get('_id')}
        # })

        self.data = data

        if driver is None:
            self.driver = SeleniumDriver(headless=headless)
        else:
            self.driver = driver

        if url is not None:
            self.driver.get(url)
        
        self.model = {}

        if sequence is None:
            print('no sequence provided')
            self.model = find_model(url if url is not None else self.driver.current_url())
            sequence = self.model['sequence']
        else:
            print('sequence provided')
        self.sequence = sequence

        if self.model.get('require_auth') is True:
            print('require_auth')
            auth = automnation.get('auth')
            if type(auth) is list:
                for cookie in auth:
                    cookie = {
                        'name': cookie.get('name'), 
                        'value': cookie.get('value')}
                    self.driver.add_cookie(cookie)
                self.driver.get(url)
                self.model = find_model(url)
                self.sequence = self.model['sequence']

        self.original_url = self.driver.current_url()
        self.model = find_model(self.driver.current_url())
        # self.sequence = self.model['sequence']

        self.website = self.model.get('website')
        
        self.item = item if item is not None else self.model['fields']()

        self.filename = filename

        self.automnation = {}
        # if sequenceid is not None:
        #     self.automnation = mongo({
        #         "db": 'tools',
        #         "collection": "automnations",
        #         "selector": {'_id': sequenceid}
        #     })
        #     self.mongo_selector = {
        #         'db': 'tools',
        #         "collection": "automnations",
        #     }

    def add_item(self, item={}):

        self.data.extend(item)

        if self.filename is not None:
            add_data_to_csv(data=[item], filename=self.filename)
            # add_data_to_json(data=[item], filename=self.filename)

        if self.automnation.get('_id') is not None:
            edit = self.update_automnation({
                "$push": {
                    'data': item
                }
            })
            if edit is True:
                print(Fore.GREEN + 'item added to storage')
                print(Style.RESET_ALL)
        
    # def update_data(self):
    #     mongo()
    #     pass

    def update_item(self, name, value):
        self.item.__setattr__(name, value)

    # AUTOMNATION                
    
    # def get_automnation(self)
    
    def update_automnation(self, updator):
        return mongo({
            "db": 'tools',
            "collection": "automnation",
            "action": "edit",
            "selector": {"_id": self.automnation.get('_id')},
            "updator": updator
        })
    
    def pause_automnation(self):
        # return mongo({
        #     "db": 'storage',
        #     "collection": "tables",
        #     "action": "edit",
        #     "selector": {"_id": self.automnation.get('_id')},
        #     "updator": {
        #         'active': False,
        #         'status': 'pause',
        #         "message": 'Automnation in pause ...'
        #     }
        # })
        pass

    def play(self) -> None:
        tzprint('play', self.depth)
        # time.sleep(2)

        # mongo({
        #     "db": 'storage',
        #     "collection": "tables",
        #     "action": "edit",
        #     "selector": {"_id": self.automnation.get('_id')},
        #     "updator": {
        #         'active': True,
        #         'status': 'active',
        #     }
        # })

        for step in self.sequence:
            
            tzprint(Fore.WHITE + 'step: ' + str(step), self.depth)
            value = self.sequence[step]

            # ---------------- ACTION ---------------------

            if ':click' in step:
                if type(value) == str:
                    self.driver.click(value)
                elif type(value) == list:
                    for e in value:
                        self.driver.click(e)
                continue

            elif ":execute_script" in step:
                if type(value) == str:
                    self.driver.execute_script(value)
                elif type(value) == list:
                    for script in value:
                        self.driver.execute_script(script)
                continue

            elif ":wait" in step:
                time.sleep(value)
                continue

            elif ":goto" in step:

                if ":original_url" in value:
                    # tzprint(Fore.WHITE + 'go back to original_url', self.depth)
                    self.driver.get(self.original_url)
                    continue

                url = ""

                if type(value) == str:
                    if "http" in value:
                        url = value
                    else:
                        url = get_element_data(
                            driver=self.driver,
                            selector=value, prop="href")
                        
                elif type(value) == dict:
                    url = get_element_data(
                        driver=self.driver,
                        selector=value['selector'],
                        prop=value['property'])
                    
                if url.strip() != "" and url is not None:
                    self.driver.get(url.strip())
                    if '404' in self.driver.current_url() or 'unavailable' in self.driver.current_url():
                        tzprint(Fore.RED + 'error', self.depth)
                        print(Style.RESET_ALL)
                        self.driver.get(
                            "/".join(self.driver.current_url().split('/')[:3]))
                        self.driver.get(url.strip())

                continue

            elif ':sequence' in step:
                seq = Sequence(
                    driver=self.driver, 
                    item=self.item, 
                    data=[], 
                    sequence=value,
                    depth= self.depth + 1)
                seq.play()
                if len(seq.data) == 1:
                    for prop in seq.data[0]:
                        if self.item.get(prop) is not None:
                            self.item[prop] = seq.data[0][prop]
                continue
                

            # ---------------- LOOPING ---------------------

            if ':loop' in step:
                
                listing = []
                i_loop = 0
                pagination = value.get('pagination')

                page = 99
                if type(value.get('page')) is str:
                    page = int(get_element_data(self.driver, value.get('page')))
                elif type(value.get('page')) is int:
                    page = value.get('page')
                print(f"page: {page}")

                if not self.driver.is_attached(str(pagination)):
                    print('pagination is not attached')
                    for _ in range(5):
                        if not self.driver.is_attached(str(pagination)):
                            time.sleep(1)

                while i_loop < page and self.driver.is_attached(str(pagination)):
                    i_loop = i_loop + 1

                    tzprint(f'page: {i_loop}/{page}')
                    if not self.driver.is_attached(str(pagination)):
                        print('pagination is not attached')
                        for _ in range(5):
                            if not self.driver.is_attached(str(pagination)):
                                time.sleep(1)
                    
                    listing_sequence = Sequence(
                        item=self.item,
                        driver=self.driver,
                        sequence=value['listing'],
                        data=[],
                        depth=self.depth + 1)
                    listing_sequence.play()

                    
                    if value.get('replace') == True:
                        listing = listing_sequence.data
                    else:
                        for data_url in listing_sequence.data:
                            if data_url not in listing:
                                listing.append(data_url)
                    
                    self.driver.click(value['pagination'])

                    tzprint(Fore.GREEN + f'+{len(listing_sequence.data)} urls to scrap', self.depth)
                    tzprint(Fore.WHITE + f'TOTAL: {len(listing)}', self.depth)

                tzprint(Fore.GREEN + f"listing ended: {str(len(listing))} urls founded", self.depth)
                print(Style.RESET_ALL)

                # for i in range(len(listing)):
                #     listing[i] = str(listing[i]).split('?')[0]
                    
                if value.get('deep') is False:
                    self.data = listing
                    continue

                for u in range(len(listing)):
                    
                    url = listing[u]
                    # next(item for item in listing if item["name"] == "Pam")

                    if type(url) == str:

                        self.driver.get(url)
                        time.sleep(1)
                        url = self.driver.current_url()
                        for attr in self.item.__dict__:
                            self.update_item(attr, "")
                            
                        model = find_model(url=url)
                        loop_sequence = Sequence(
                            driver=self.driver, 
                            sequence=model.get('sequence'),
                            depth=self.depth + 1)
                        loop_sequence.play()

                        model = loop_sequence.model
                        loop_sequence.update_item("SOURCE_URL", url)
                        item = loop_sequence.item.__dict__
                        pprint(item)
                        
                        print(Fore.GREEN + f"+1 item scrapped ({u + 1}/{len(listing)})")
                        item_exist = False
                        # item_exist_dict = {}
                        # print(str(self.data))
                        # print(Fore.WHITE + f"data: {self.data}")
                        for key in item:
                            if 'EMAIL' in key or 'PHONE' in key:
                                if item[key] != '' and item[key] in str(self.data):
                                    # print(Fore.WHITE + f"data: {self.data}")
                                    # print(Fore.WHITE + f"item[key]: {item[key]}")
                                    item_exist = True
                                    # item_exist_dict = item
                                    break
                        if item_exist:
                            # print(Fore.WHITE + f"data: {self.data}")
                            print(Fore.RED + f"item already exist")
                            print(Style.RESET_ALL)
                            continue
                        self.add_item(item)
                        print(f"item added to data")
                        print(Style.RESET_ALL)

                    print(Style.RESET_ALL)
                continue
                
            # ---------------- GET DATA ---------------------

            step_property = str(step).split(':')[0]

            if step_property != '':
                if self.item.get(step_property) is None:
                    tzprint(Fore.RED + f'{step_property} is an incorrect attribute', self.depth)
                    continue
                elif self.item.get(step_property) != '':
                    print(Fore.RED + f'property {step_property} is already set')
                    continue

            if ":find" in step:
                result = ''

                if type(value) == dict:

                    name = self.item.get('COMPANY_NAME')
                    if value.get('name') is not None:
                        name = get_element_data(driver=self.driver, selector=value.get('name'))
                    # print(name)

                    location = self.item.get('COMPANY_LOCATION')
                    if value.get('location') is not None:
                        location = get_element_data(driver=self.driver, selector=value.get('location'))
                    # print(location)

                    finder = Finder(
                        driver=self.driver,
                        name=name,
                        location=location,
                    )

                    if ":contact" in step:
                        result = str(finder.email())
                        result = str(finder.phone())
                        result = str(finder.website())
                        result = str(finder.linkedin())
                        result = str(finder.indeed())
                        result = str(finder.facebook())
                        result = str(finder.youtube())

                    if ":email" in step:
                        result = str(finder.email())
                    elif ":phone" in step:
                        result = str(finder.phone())
                    elif ':website' in step:
                        result = str(finder.website())
                    elif ':linkedin' in step:
                        result = str(finder.linkedin())
                    elif ':indeed' in step:
                        result = str(finder.indeed())
                    elif ':facebook' in step:
                        result = str(finder.facebook())
                    elif ':facebook' in step:
                        result = str(finder.youtube())
                    else:
                        continue

                    self.update_item(step_property, result)

                self.driver.get(self.original_url)

            elif ':get' in step:

                if step_property == "":
                    if ":all" in step:
                        v = {}
                        if type(value) == str:
                            v = get_elements_data(
                                driver=self.driver, selector=value, prop="innerText")
                        elif type(value) == dict:
                            v = get_elements_data(
                                driver=self.driver,
                                selector=value['selector'],
                                prop=value['property'])
                            
                        self.data.extend(v.copy())
                        continue
                    else:
                        tzprint(Fore.RED + 'Nothing to get all', self.depth)

                else:

                    if ":current_url" in step:
                        self.update_item(
                            step_property, 
                            self.driver.current_url())
                        continue

                    if type(value) == str:
                        self.update_item(
                            step_property, 
                            get_element_data(driver=self.driver, selector=value, prop="innerText"))
                        
                    elif type(value) == dict or value.get('selector') is not None:
                        self.update_item(step_property, get_element_data(
                            driver=self.driver,
                            selector=value.get('selector'),
                            prop=value.get('property') if value.get('property') is not None else 'innerText'))
                        if value.get('replace') == str:
                            self.update_item(
                                step_property, 
                                re.sub(value.get('replace', ''), '', self.item.__getattribute__(step_property)))
                        # print(Fore.GREEN + self.item.__getattribute__(step_property))
                    else:
                        print(Fore.RED + 'Nothing to get')

            print(Style.RESET_ALL)
        print(Style.RESET_ALL)

        # if len(list(self.item)) > 0:
        #     self.data.append(self.item.copy())

        tzprint(self.chrono.end(), self.depth)

        # mongo({
        #     "db": 'storage',
        #     "collection": "tables",
        #     "action": "edit",
        #     "selector": {"_id": self.automnation.get('_id')},
        #     "updator": {
        #         'active': False,
        #         'status': 'Finished',
        #     }
        # })

        return
