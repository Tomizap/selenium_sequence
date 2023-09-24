import threading
import time

from flask import Flask, request
from selenium_sequence import Sequence, find_model
from selenium_driver import SeleniumDriver

app = Flask(__name__)


@app.route('/sequence', methods=['OPTIONS'])
def options_sequence():
    url = request.json.get('url')
    return find_model(url=url)



@app.route('/sequence/play', methods=['POST'])
def play_sequence():
    _id = request.json.get('_id')

    urls = request.json.get('urls')
    # auth = request.json.get('auth')

    # data = []
    threads = []
        
    for url in urls:
        s = Sequence(
            url=url, 
            auth=request.json.get('auth'), 
            filename=None)
        thread = threading.Thread(target=s.play)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "ok": True,
        "data": []
    }


@app.route('/sequence/autoapply', methods=['POST'])
def play_sequence():
    url = request.json.get('url')
    auth = request.json.get('auth')
        
    sequence = Sequence(url=url, auth=auth)
    sequence.play()

    data = sequence.data
    return data


# @app.route('/scrapper', methods=['OPTIONS'])
# def options_sequence():
#     url = request.json.get('url')
#     return find_model(url=url)


if __name__ == '__main__':
    app.run()
