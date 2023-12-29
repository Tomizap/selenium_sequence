from pprint import pprint
import re
import time
from colorama import Fore, Style
from selenium_driver import SeleniumDriver
from tzmongo import mongo

from selenium_sequence.data import get_element_data, get_elements_data
from selenium_sequence.finder import Finder
from selenium_sequence.items import *
from selenium_sequence.models import find_model


class Sequence:
  
  def __init__(self, 
               driver=None, 
               model={}, 
               steps=None, 
               source_url="", 
               data=None, 
               item=None, 
               automnation_id=None, 
               storage=None) -> None:
    print(Fore.WHITE + 'init Sequence')
    
    self.source_url = source_url
    self.driver = driver if driver is not None else SeleniumDriver()
    self.model = model if len(model) > 0 else find_model(url=source_url)
    if steps is not None:
        self.model['steps'] = steps
    self.item = item if item is not None else find_model(url=source_url).get('fields', Item)()
    self.automnation_id = automnation_id

    self.data = data if type(data) == list else []

  # -------------- AUTOMNATION ------------------

  def get_automnation(self) -> dict:
      if self.automnation_id is not None:
          return {}
      getting = mongo({
            "collection": "automnations",
            "selector": {'_id': self.automnation_id}
        })
      if getting.get('ok', False) is True:
          pprint(getting)
          return getting.get('data', [{}])[0]
      else:
          print('error')
          return {}
      
  def update_automnation(self, setter={}) -> None:
      if self.automnation_id is None:
          return
      mongo({
          "collection": "automnations",
          "action": "edit",
          "selector": {"_id": self.automnation_id},
          "updator": {
              '$set': setter
          }
      })

  # -------------- STORAGE ------------------
  
  def add_data(self, item={}) -> None:
        
        if len(item) == 0:
            print(Fore.RED + 'no item')
            return
      
        if self.item_exist(item=item):
            print(Fore.RED + 'item already exist')
            return
        
        adding = mongo({
            'db': "contacts",
            "collection": "companies",
            "action": "add",
            "selector": item
        })
        if adding.get('ok', False) is False:
            print(adding)
            print(Fore.RED + "MongoError: " + str(adding.get('message')))
        else:
            print(Fore.GREEN + f"item successfully added to mongo")

        print(Style.RESET_ALL)

  # -------------- ITEM ------------------

  def update_item(self, name, value) -> None:
      self.item.__setattr__(name, value)

  def item_exist(self, item={}) -> bool:
    # print('item_exist')
    # item = item.__dict__
    try:
        COMPANY_PHONE = item.get('COMPANY_PHONE', '') if item.get('COMPANY_PHONE', '') != '' else 0
        # COMPANY_EMAIL = item.get('COMPANY_EMAIL', '') if item.get('COMPANY_EMAIL', '') != '' else 0
        SOURCE_URL = item.get('SOURCE_URL', '') if item.get('SOURCE_URL', '') != '' else 0
        ie = mongo({
            "db": "contacts",
            'collection': "companies",
            'selector': {
                "$or": [
                    {"COMPANY_PHONE": COMPANY_PHONE}, 
                    # {"COMPANY_EMAIL": COMPANY_EMAIL}, 
                    {"SOURCE_URL": SOURCE_URL}, 
                ]
            }
        })
        return len(list(ie.get('data', []))) > 0
    except Exception as e:
        print(str(e))
        return True

  # -------------- RUNNING ------------------

  def play(self):
    print('play sequence')
    sequence = self.model.get('steps', {})
    original_url = self.source_url

    for step in sequence:
                
        print(Fore.WHITE + 'step: ' + str(step))
        value = sequence[step]

        if self.item_exist(item=self.item.__dict__):
            # print(Fore.WHITE + f"data: {self.data}")
            print(Fore.RED + f"item already exist")
            print(Style.RESET_ALL)
            break

        try:
        
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
                    # print(Fore.WHITE + 'go back to original_url')
                    self.driver.get(original_url)
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
                        print(Fore.RED + 'error')
                        print(Style.RESET_ALL)
                        self.driver.get(
                            "/".join(self.driver.current_url().split('/')[:3]))
                        self.driver.get(url.strip())

                continue

            elif ':sequence' in step:
                seq = Sequence(
                    driver=self.driver, 
                    item=self.item,
                    steps=value,
                    data=[])
                seq.play()
                if len(seq.data) == 1:
                    for prop in seq.data[0]:
                        if self.item.get(prop) is not None:
                            self.item.__setattr__(prop, seq.data[0][prop])
                            # self.item[prop] = seq.data[0][prop]
                continue

            if ':loop' in step:
                
                listing = []
                pagination = value.get('pagination', value.get('pagination:not'))
                i_loop = 0

                page = 99
                if type(value.get('page')) is str:
                    page = int(get_element_data(self.driver, value.get('page')))
                elif type(value.get('page')) is int:
                    page = value.get('page')

                if not self.driver.is_attached(str(pagination)) and "pagination:not" not in str(value):
                    for _ in range(5):
                        if not self.driver.is_attached(str(pagination)):
                            time.sleep(1)
                    print(Fore.RED + 'pagination is not attached')
                    print(Style.RESET_ALL)
                    continue

                same_retry = 0
                while i_loop < page and (not self.driver.is_attached(str(pagination)) if "pagination:not" in str(value) else self.driver.is_attached(str(pagination))):
                    i_loop = i_loop + 1
                    print(f'page: {i_loop}/{page}')
                    
                    listing_sequence = Sequence(
                        item=self.item,
                        driver=self.driver,
                        automnation_id=self.automnation_id,
                        data=[],
                        steps=value['listing'])
                    listing_sequence.play()
                    
                    url_added = 0

                    old_listing = listing
                    if value.get('replace') == True:
                        listing = listing_sequence.data.copy()
                        if len(old_listing) == len(listing):
                            print(Fore.RED + "no url added to listing")
                            same_retry = same_retry + 1
                            if same_retry == 5:
                                print(Fore.RED + "breaking listing because: to much same_retry")
                                print(Style.RESET_ALL)
                                break
                        else:
                            same_retry = 0
                            url_added = len(listing) - len(old_listing)

                    else:
                        for listing_url in listing_sequence.data.copy():
                            if listing_url not in listing and listing_url not in str(self.data):
                                listing.append(listing_url)
                                url_added = url_added + 1
                            else:
                                print(Fore.RED + f"item already exist")
                                print(Style.RESET_ALL) 

                    print(Fore.GREEN + f'+{url_added} urls of {len(listing)} to scrap')
                    print(Style.RESET_ALL)

                    if "pagination:not" not in str(value):
                        if not self.driver.is_attached(str(pagination)):
                            for _ in range(5):
                                if not self.driver.is_attached(str(pagination)):
                                    time.sleep(1)
                            print(Fore.RED + 'pagination is not attached')
                            print(Style.RESET_ALL)
                        if page != 1:
                            self.driver.click(value.get('pagination', 'body'))

                print(Fore.GREEN + f"listing ended: {str(len(listing))} urls founded")
                print(Style.RESET_ALL)
                    
                if value.get('deep') is False:
                    self.data = listing
                    continue

                for u in range(len(listing)):
                    
                    url = listing[u]

                    if self.item_exist({"SOURCE_URL": url}):
                        print(Fore.RED + f"item already exist")
                        print(Style.RESET_ALL)
                        continue

                    if type(url) == str:

                        self.driver.get(url)
                        time.sleep(1)

                        for attr in self.item.__dict__:
                            self.update_item(attr, "")                 
                    
                        loop_sequence = Sequence(
                            source_url=url,
                            driver=self.driver, 
                            steps=find_model(url=url).get('steps', {}),
                            automnation_id=self.automnation_id)
                        loop_sequence.play()
                        
                        loop_sequence.update_item("SOURCE_URL", url)
                        item = loop_sequence.item.__dict__

                        pprint(item)
                        print(Fore.GREEN + f"+1 item scrapped ({u + 1}/{len(listing)})")
                        print(Style.RESET_ALL)
                        
                        self.add_data(item=item)

                    print(Style.RESET_ALL)
                    
                print(Style.RESET_ALL)
                continue
                
            # ---------------- GET DATA ---------------------

            step_property = str(step).split(':')[0]

            # print(self.item.__dict__)
            if step_property != '':
                if self.item.get(name=step_property) is None:
                    print(Fore.RED + f'{step_property} is an incorrect attribute')
                    continue
                elif self.item.get(name=step_property) != '':
                    print(Fore.RED + f'property {step_property} is already set')
                    continue

            if ":find" in step:
                result = ''

                if type(value) == dict:

                    website = self.item.get('COMPANY_WEBSITE_URL')
                    if value.get('website') is not None:
                        website = get_element_data(driver=self.driver, selector=value.get('website'))

                    name = self.item.get('COMPANY_NAME')
                    if value.get('name') is not None:
                        name = get_element_data(driver=self.driver, selector=value.get('name'))

                    location = self.item.get('COMPANY_LOCATION')
                    if value.get('location') is not None:
                        location = get_element_data(driver=self.driver, selector=value.get('location'))

                    finder = Finder(
                        name=name,
                        location=location,
                    )

                    # if ":contact" in step:
                    #     result = str(finder.email())
                    #     result = str(finder.phone())
                    #     result = str(finder.website())
                    #     result = str(finder.linkedin())
                    #     result = str(finder.indeed())
                    #     result = str(finder.facebook())
                    #     result = str(finder.youtube())

                    #     self.update_item(name=value.get('prefix', "") + "EMAIL", value=str(finder.email()))

                    if ":email" in step:
                        result = str(finder.email())
                    elif ":phone" in step:
                        result = str(finder.phone())
                    elif ':website' in step:
                        result = str(finder.website())
                    # elif ':linkedin' in step:
                    #     result = str(finder.linkedin())
                    # elif ':indeed' in step:
                    #     result = str(finder.indeed())
                    # elif ':facebook' in step:
                    #     result = str(finder.facebook())
                    # elif ':facebook' in step:
                    #     result = str(finder.youtube())
                    
                    else:
                        continue

                    self.update_item(step_property, result)

                    finder.close()

            elif ':get' in step:
                # print('get')

                if step_property == "":
                    if ":all" in step:
                        # print(':all')
                        # pprint(value)
                        v = {}
                        if type(value) == str:
                            v = get_elements_data(
                                driver=self.driver, selector=value, prop="innerText")
                        elif type(value) == dict:
                            v = get_elements_data(
                                driver=self.driver,
                                selector=value['selector'],
                                prop=value['property'])
                        
                        # print("v.copy()", type(v.copy()), v.copy())
                        self.data.extend(v.copy())
                        continue
                    else:
                        print(Fore.RED + 'Nothing to get all')

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

        except Exception as e:
            print(Fore.RED + f"Error in {str(step)}: {str(e)}")

    print(Style.RESET_ALL)