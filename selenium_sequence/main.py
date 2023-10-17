import threading
from colorama import Fore, Style
from selenium_driver import SeleniumDriver
from tzmongo import mongo

# from selenium_sequence.finder import Finder
from selenium_sequence.sequence import Sequence

from .models import find_model
from .chrono import Chronos
from .items import *
from .tzprint import *
# from .automnation import *


class Automnation:

    def __init__(
            self, 
            driver=None, 
            # item=None, 
            depth=0,
            headless=True,
            filename=None,
            _id=None,
            urls=None, 
            data=[], 
            sequence=None) -> None:

        self.chrono = Chronos()
        self.chrono.start()

        self.depth = depth
        print(f'init Automnation')

        if driver is None:
            self.driver = SeleniumDriver(headless=headless)
        else:
            self.driver = driver

        self.data = []
        self.automnation = None
        if _id is not None:
            ga = mongo({
                'collection': 'automnations',
                "selector": {'_id': _id}
            })
            # print(ga)
            if ga['ok'] == True:
                self.automnation = ga['data'][0]
            self.data = data

        self.urls = [self.driver.current_url()]
        if urls is not None:
            if type(urls) == str:
                self.urls = [urls]
            elif type(urls) == list:
                self.urls = urls
        elif self.automnation is not None:
            self.urls = self.automnation.get('urls', [])

        self.sequence = None
        if sequence is not None:
            print('sequence is provided')
            # print(sequence)
            self.sequence = sequence

        # self.filename = filename

    def pause(self) -> dict:
        if self.automnation is not None:
            mongo({
                "collection": "automnations",
                "selector": {'_id': self.automnation.get('_id')},
                "action": "edit",
                "updator": {
                    "$set": {
                        "active": False,
                        "status": 'inactive',
                        'message': "Pause"
                    }
                }
            })
            return {
                "ok":True,
                "data": [],
                'message': 'automnation en pause'
            }
        return {
            "ok": False,
            "data": [],
            'message': 'pas d\'automnation'
        }
    
    def stop(self) -> dict:
        if self.automnation is not None:
            mongo({
                "collection": "automnations",
                "selector": {'_id': self.automnation.get('_id')},
                "action": "edit",
                "updator": {
                    "$set": {
                        "active": False,
                        "status": 'inactive',
                        'message': "Automnation has been stoped"
                    }
                }
            })
            return {
                "ok":True,
                "data": [],
                'message': 'Automnation has been stoped'
            }
        return {
            "ok": False,
            "data": [],
            'message': 'pas d\'automnation'
        }

    def play(self) -> dict:

        if self.automnation is not None:
            mongo({
                "collection": "automnations",
                "selector": {'_id': self.automnation.get('_id')},
                "action": "edit",
                "updator": {
                    "$set": {
                        "active": True,
                        "status": 'active'
                    }
                }
            })

        urls = self.urls
        print(f'{len(urls)} source_url to scrap')

        threads = []
        for url in urls:

            if url != self.driver.current_url():
                self.driver.get(url)

            model = find_model(url)

            if model.get('require_auth') is True and self.automnation is not None:
                print('require_auth')
                auth = self.automnation.get('auth', [])
                for cookie in auth:
                    cookie = {
                        'name': cookie.get('name'), 
                        'value': cookie.get('value')}
                    self.driver.add_cookie(cookie)
                self.driver.get(url)

            main_sequence = Sequence(
                driver=self.driver,
                steps=model.get('steps', {}),
                source_url=url,
                item=model.get('fields', Item)(),
                automnation_id=self.automnation.get('_id') if self.automnation is not None else '',
            )
            main_sequence.play()
            # thread = threading.Thread(target=main_sequence.play)
            # thread.start()
            # threads.append(thread)
        
        # for thread in threads:
        #     thread.start()

        print(Style.RESET_ALL)

        tzprint(self.chrono.end(), self.depth)

        if self.automnation is not None:
            mongo({
                "collection": "automnations",
                "selector": {'_id': self.automnation.get('_id')},
                "action": "edit",
                "updator": {
                    "$set": {
                        "active": False,
                        "status": 'inactive'
                    }
                }
            })

        return {
            'ok': True,
            'data': [],
            "message": "L'Automnation a bien été lancée"
        }
