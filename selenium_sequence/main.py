import queue
import threading
import time
from colorama import Fore, Style
from selenium_driver import SeleniumDriver
from tzmongo import mongo

from selenium_sequence.sequence import Sequence

from .models import find_model
from .chrono import Chronos
from .items import *

NB_MAX_THREADS = 30


class Automnation:

    def __init__(
            self,
            headless=True,
            _id=None,
            urls=None) -> None:

        print(f'init Automnation')

        self.chrono = Chronos()
        self.chrono.start()
        
        self.url_queue = queue.Queue()

        self.headless = headless
        
        self.automnation = None
        if _id is not None:
            ga = mongo({
                'collection': 'automnations',
                "selector": {'_id': _id}
            })
            # print(ga)
            if ga['ok'] == True:
                self.automnation = ga['data'][0]
            
        self.urls = []
        if urls is not None:
            if type(urls) == str:
                self.urls = [urls]
            elif type(urls) == list:
                self.urls = urls
        elif self.automnation is not None:
            self.urls = self.automnation.get('urls', [])

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

    def worker(self, url):

        driver = SeleniumDriver(headless=self.headless)
        driver.get(url)
        model = find_model(url)

        # if model.get('require_auth') is True and self.automnation is not None:
        #     print('require_auth')
        #     auth = self.automnation.get('auth', [])
        #     for cookie in auth:
        #         cookie = {
        #             'name': cookie.get('name'), 
        #             'value': cookie.get('value')}
        #         driver.add_cookie(cookie)
        #     driver.get(url)

        sequence = Sequence(
            driver=driver,
            source_url=url,
            steps=model.get('steps', {}),
            item=model.get('fields', Item)(),
            automnation_id=self.automnation.get('_id') if self.automnation is not None else '',
            storage=self.automnation.get('storage') if self.automnation is not None else ''
        )
        sequence.play()
        driver.close()

    def thread_runner(self):
        while True:
            try:
                url = self.url_queue.get(block=False)
                self.worker(url)
                self.url_queue.task_done()

            except queue.Empty:
                print('queue.Empty')
                break

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
            
        print(f'{len(self.urls)} source_url to scrap')
        
        for url in self.urls:
            self.url_queue.put(url)
            
        active_threads = []

        for _ in range(NB_MAX_THREADS):
            thread = threading.Thread(target=self.thread_runner)
            thread.start()
            active_threads.append(thread)

        self.url_queue.join()

        print(Style.RESET_ALL)

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

        self.chrono.end()

        return {
            'ok': True,
            'data': [],
            "message": "L'Automnation a bien été lancée"
        }
