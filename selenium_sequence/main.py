import time
from pprint import pprint

from colorama import Fore, Style
from selenium_driver import SeleniumDriver

from .models import find_model
# from .finder import Finder
from .data import get_element_data, get_elements_data
from .chrono import Chronos
from .csv_script import add_data_to_csv


class Sequence:

    def __init__(self, driver=None, url=None, item=None, data=None, sequence=None, filename=None):
        if data is None:
            data = []
        if item is None:
            item = {}
        self.chrono = Chronos()
        self.chrono.start()
        self.driver = driver
        if self.driver is None:
            self.driver = SeleniumDriver()
        if url is not None:
            self.driver.get(url)
        self.item = item
        self.data = data
        self.filename = filename
        self.original_url = driver.current_url()
        self.model = find_model(self.original_url)
        if sequence is None:
            self.sequence = self.model['sequence']
        return

    def play(self):

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
                continue

            elif ":execute_script" in step:
                if type(value) == str:
                    self.driver.execute_script(value)
                elif type(value) == list:
                    for script in value:
                        self.driver.execute_script(script)

            elif ":wait" in step:
                time.sleep(value)
                continue

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
                        time.sleep(3)
                        if '404' in self.driver.current_url() or 'unavailable' in self.driver.current_url():
                            print(Fore.RED, 'error')
                            print(Style.RESET_ALL)
                            self.driver.get(
                                "/".join(self.driver.current_url().split('/')[:3]))
                            time.sleep(3)
                            self.driver.get(url.strip())
                            time.sleep(3)
                continue

            elif ':sequence' in step:
                ps = play_sequence(
                    driver=self.driver, item={}, data=[], sequence=value)
                if len(ps) == 1:
                    for prop in ps[0]:
                        self.item[prop] = ps[0][prop]

            # ---------------- SCRAPPING ---------------------

            elif ':loop' in step:
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
                    pi = play_sequence(
                        driver=self.driver,
                        sequence=value['listing'],
                        data=[])
                    listing.extend(pi.copy())
                    print(
                        Fore.GREEN + f"+{len(pi)} url{'s' if len(pi) > 1 else ''} (page {i_page_number} / {page_number})")
                print(Fore.GREEN + str(len(listing)) + " urls founded")
                print(Style.RESET_ALL)
                for e in range(len(listing)):
                    time.sleep(3)
                    if type(listing[e]) == str:
                        # print('link_loop' + str(listing[e]))
                        items_loop = play_sequence(driver=self.driver, url=listing[e], data=[], item={
                            "URL": self.driver.current_url()
                        }, sequence=find_model(listing[e])['sequence'])
                        # items_loop['URL'] = driver.current_url()
                        pprint(items_loop[0])
                        try:
                            add_data_to_csv(items_loop, "D:/PythonPackages/selenium_scrapper/data/", self.filename)
                        except:
                            pass
                        if len(items_loop) == 1:
                            self.data.append(items_loop[0].copy())
                        elif len(items_loop) > 1:
                            self.data.extend(items_loop)
                    print(Fore.GREEN + f"+1 item ({e + 1}/{len(listing)})")

            elif ":find" in step:
                # continue
                result = ''
                #     finder = Finder(
                #         name=get_element_data(driver=driver, selector=value['name']),
                #         title=get_element_data(driver=driver, selector=value['title']),
                #         location=get_element_data(driver=driver, selector=value['location']))
                #     if ":email" in step:
                #         result = str(finder.email())
                #         print(Fore.WHITE + result)
                #     elif ":phone" in step:
                #         result = str(finder.phone())
                #         print(Fore.WHITE + result)
                self.item[value['property']] = result
                continue

            elif ':get' in step:
                if step_property == "":
                    if ":all" in step:
                        v = {}
                        if type(value) == str:
                            v = get_elements_data(
                                driver=self.driver, selector=value['selector'], prop="innerText")
                        elif type(value) == dict:
                            v = get_elements_data(
                                driver=self.driver,
                                selector=value['selector'],
                                prop=value['property'])
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
                    continue

            print(Style.RESET_ALL)
        if len(list(self.item)) > 0:
            self.data.append(self.item.copy())
        print(self.chrono.end())
        return

    def data(self):
        return self.data


def play_sequence(driver=None, url=None, item=None, data=None, sequence=None, filename=None):

    print(Style.RESET_ALL)
    print('play_sequence()')
    chrono = Chronos()
    chrono.start()
    if data is None:
        data = []
    if item is None:
        item = {}
    if driver is None:
        # print(Fore.RED + 'no driver')
        driver = SeleniumDriver()
    if url is not None:
        driver.get(url)
    original_url = driver.current_url()
    fm = find_model(original_url)
    if sequence is None:
        sequence = fm['sequence']
    time.sleep(3)

    for step in sequence:
        value = sequence[step]
        step_property = str(step).split(':')[0]
        print(Fore.WHITE + '- step: ' + str(step))

        # ---------------- ACTION ---------------------

        if ':click' in step:
            # print(value)
            if type(value) == str:
                driver.click(value)
            elif type(value) == list:
                for e in value:
                    driver.click(e)
            continue

        elif ":execute_script" in step:
            if type(value) == str:
                driver.execute_script(value)
            elif type(value) == list:
                for script in value:
                    driver.execute_script(script)

        elif ":wait" in step:
            time.sleep(value)
            continue

        elif ":goto" in step:
            if ":original_url" in value:
                print(Fore.WHITE + 'go back to original_url')
                driver.get(original_url)
            else:
                url = ""
                if type(value) == str:
                    if "http" in value:
                        url = value
                    else:
                        url = get_element_data(
                            driver=driver,
                            selector=value, prop="href")
                elif type(value) == dict:
                    url = get_element_data(
                        driver=driver,
                        selector=value['selector'],
                        prop=value['property'])
                # print(url)
                if url.strip() != "" and url is not None:
                    # print(url)
                    driver.get(url.strip())
                    time.sleep(3)
                    if '404' in driver.current_url() or 'unavailable' in driver.current_url():
                        print(Fore.RED, 'error')
                        print(Style.RESET_ALL)
                        driver.get(
                            "/".join(driver.current_url().split('/')[:3]))
                        time.sleep(3)
                        driver.get(url.strip())
                        time.sleep(3)
            continue

        elif ':sequence' in step:
            ps = play_sequence(
                driver=driver, item={}, data=[], sequence=value)
            if len(ps) == 1:
                for prop in ps[0]:
                    item[prop] = ps[0][prop]

        # ---------------- SCRAPPING ---------------------

        elif ':loop' in step:
            listing = []
            page_number = 0
            if type(value['pagination']) == int:
                page_number = value['pagination']
            elif type(value['pagination']) == str:
                try:
                    page_number = int(get_element_data(driver=driver, selector=value['pagination']))
                except:
                    page_number = 40
            for i_page_number in range(page_number):
                pi = play_sequence(
                    driver=driver,
                    sequence=value['listing'],
                    data=[])
                listing.extend(pi.copy())
                print(Fore.GREEN + f"+{len(pi)} url{'s' if len(pi) > 1 else ''} (page {i_page_number} / {page_number})")
            print(Fore.GREEN + str(len(listing)) + " urls founded")
            print(Style.RESET_ALL)
            for e in range(len(listing)):
                time.sleep(3)
                if type(listing[e]) == str:
                    # print('link_loop' + str(listing[e]))
                    items_loop = play_sequence(driver=driver, url=listing[e], data=[], item={
                        "URL": driver.current_url()
                    }, sequence=find_model(listing[e])['sequence'])
                    # items_loop['URL'] = driver.current_url()
                    pprint(items_loop[0])
                    add_data_to_csv(items_loop, "D:/PythonPackages/selenium_scrapper/data/", filename)
                    if len(items_loop) == 1:
                        data.append(items_loop[0].copy())
                    elif len(items_loop) > 1:
                        data.extend(items_loop)
                print(Fore.GREEN + f"+1 item ({e+1}/{len(listing)})")

        elif ":find" in step:
            # continue
            result = ''
        #     finder = Finder(
        #         name=get_element_data(driver=driver, selector=value['name']),
        #         title=get_element_data(driver=driver, selector=value['title']),
        #         location=get_element_data(driver=driver, selector=value['location']))
        #     if ":email" in step:
        #         result = str(finder.email())
        #         print(Fore.WHITE + result)
        #     elif ":phone" in step:
        #         result = str(finder.phone())
        #         print(Fore.WHITE + result)
            item[value['property']] = result
            continue

        elif ':get' in step:
            if step_property == "":
                if ":all" in step:
                    v = {}
                    if type(value) == str:
                        v = get_elements_data(
                            driver=driver, selector=value['selector'], prop="innerText")
                    elif type(value) == dict:
                        v = get_elements_data(
                            driver=driver,
                            selector=value['selector'],
                            prop=value['property'])
                    data.extend(v.copy())
                    continue
                else:
                    print(Fore.RED + 'Nothing to get all')
            else:
                if type(value) == str:
                    item[step_property] = get_element_data(
                        driver=driver, selector=value, prop="innerText")
                elif type(value) == dict:
                    item[step_property] = get_element_data(
                        driver=driver,
                        selector=value['selector'],
                        prop=value['property'])
                else:
                    print(Fore.RED + 'Nothing to get')
                continue

        print(Style.RESET_ALL)
    if len(list(item)) > 0:
        data.append(item.copy())
    print(chrono.end())
    return data
