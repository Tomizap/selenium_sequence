import time
from pprint import pprint

from colorama import Fore, Style
from selenium_driver import SeleniumDriver

from selenium_sequence.finder import Finder

from .models import find_model
from .data import get_element_data, get_elements_data
from .chrono import Chronos
# from .csv_script import add_data_to_csv


class Sequence:

    def __init__(self, driver=None, url=None, item=None, data=None, sequence=None, auth=None) -> None:

        self.chrono = Chronos()
        self.chrono.start()

        if data is None:
            data = []
        self.data = data

        if item is None:
            item = {}
        self.item = item

        if driver is None:
            driver = SeleniumDriver()
        self.driver = driver

        if url is not None:
            self.driver.get(url)
        self.original_url = self.driver.current_url()

        if type(auth) is list:
            for cookie in auth:
                cookie = {'name': cookie.get('name'), 'value': cookie.get('value')}
                self.driver.add_cookie(cookie)
            self.driver.get(url)
        elif type(auth) is str:
            if auth == 'indeed.com':
                pass
            if auth == 'pole-emploi.com':
                pass

        self.filename = None

        self.model = find_model(self.original_url)
        self.sequence = sequence
        if self.sequence is None:
            self.sequence = self.model['sequence']

        return

    def update_sequence(self):
        pass

    def play(self) -> None:
        # print('play')
        # time.sleep(1)
        for step in self.sequence:
            
            value = self.sequence[step]
            step_property = str(step).split(':')[0]
            print(Fore.WHITE + '- step: ' + str(step))

            # ---------------- ACTION ---------------------

            if ':click' in step:
                # print(value)
                if type(value) == str:
                    self.driver.click(value)
                elif type(value) == list:
                    for e in value:
                        self.driver.click(e)

            elif ":execute_script" in step:
                if type(value) == str:
                    self.driver.execute_script(value)
                elif type(value) == list:
                    for script in value:
                        self.driver.execute_script(script)

            elif ":wait" in step:
                time.sleep(value)

            elif ":goto" in step:
                if ":original_url" in value:
                    print(Fore.WHITE + 'go back to original_url')
                    self.driver.get(self.original_url)
                else:
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
                    # print(url)
                    if url.strip() != "" and url is not None:
                        # print(url)
                        self.driver.get(url.strip())
                        # time.sleep(3)
                        if '404' in self.driver.current_url() or 'unavailable' in self.driver.current_url():
                            print(Fore.RED, 'error')
                            print(Style.RESET_ALL)
                            self.driver.get(
                                "/".join(self.driver.current_url().split('/')[:3]))
                            # time.sleep(3)
                            self.driver.get(url.strip())
                            # time.sleep(3)

            elif ':sequence' in step:
                seq = Sequence(
                    driver=self.driver, item={}, data=[], sequence=value)
                seq.play()
                if len(seq.data) == 1:
                    for prop in seq.data[0]:
                        self.item[prop] = seq.data[0][prop]

            # ---------------- SCRAPPING ---------------------

            elif ':loop' in step:
                
                time.sleep(1)
                listing = []
                page_number = 0

                if type(value['pagination']) == int:
                    page_number = value['pagination']
                elif type(value['pagination']) == str:
                    try:
                        page_number = int(get_element_data(driver=self.driver, selector=value['pagination']))
                    except:
                        page_number = 40

                for i_page_number in range(page_number):
                    listing_sequence = Sequence(
                        driver=self.driver,
                        sequence=value['listing'],
                        data=[])
                    listing_sequence.play()
                    listing.extend(listing_sequence.data.copy())
                    # print(
                    #     Fore.GREEN + f"+{len(lseq.data)} url{'s' if len(lseq.data) > 1 else ''} (page {i_page_number} / {page_number})")
                print(Fore.GREEN + str(len(listing)) + " urls founded")
                print(Style.RESET_ALL)

                for i in range(len(listing)):
                    listing[i] = str(listing[i]).split('?')[0]
                    
                if value.get('deep') is False:
                    self.data = listing
                    continue

                # print(listing)

                for e in range(len(listing)):
                    # time.sleep(3)
                    if type(listing[e]) == str:
                        # print('link_loop' + str(listing[e]))
                        try:
                            sequence_loop = Sequence(driver=self.driver, url=listing[e], data=[], item={
                                "URL": self.driver.current_url()
                            }, sequence=find_model(listing[e])['sequence'])
                        except:
                            continue
                    
                        sequence_loop.play()
                        items_loop = sequence_loop.data
                        # items_loop['URL'] = driver.current_url()
                        pprint(items_loop[0])
                        # add_data_to_csv(items_loop, "D:/python/packages/selenium_scrapper/data/", self.filename)
                        # try:
                        #     add_data_to_csv(items_loop, "D:/PythonPackages/selenium_scrapper/data/", self.filename)
                        # except Exception as e:
                        #     print(str(e))
                        #     pass
                        if len(items_loop) == 1:
                            self.data.append(items_loop[0].copy())
                        elif len(items_loop) > 1:
                            self.data.extend(items_loop)
                    print(Fore.GREEN + f"+1 item ({e + 1}/{len(listing)})")
                

            elif ":find" in step:
                result = ''
                # print('--------')
                # print(value)
                # print(type(value))
                # print(value.get('name'))
                # print(value[0])
                # print(value[0][1])
                if type(value) == dict:
                    name = get_element_data(driver=self.driver, selector=value.get('name'))
                    location = get_element_data(driver=self.driver, selector=value.get('location'))
                    finder = Finder(
                        driver=self.driver,
                        name=name,
                        location=location,
                    )
                    if ":email" in step:
                        result = str(finder.email())
                    elif ":phone" in step:
                        result = str(finder.phone())
                        # print(Fore.WHITE + result)
                self.item[step_property if step_property != "" else value['property']] = result
                # print('--------')

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
                            # print(v)
                            
                        self.data.extend(v.copy())
                        continue
                    else:
                        print(Fore.RED + 'Nothing to get all')
                else:
                    if type(value) == str:
                        self.item[step_property] = get_element_data(
                            driver=self.driver, selector=value, prop="innerText")
                    elif type(value) == dict:
                        self.item[step_property] = get_element_data(
                            driver=self.driver,
                            selector=value['selector'],
                            prop=value['property'])
                    else:
                        print(Fore.RED + 'Nothing to get')

            print(Style.RESET_ALL)

        if len(list(self.item)) > 0:
            self.data.append(self.item.copy())

        print(self.chrono.end())

        return
