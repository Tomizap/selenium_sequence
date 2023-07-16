import time

from flask import Flask, request
from selenium_sequence import Sequence, find_model
from selenium_driver import SeleniumDriver

app = Flask(__name__)


@app.route('/sequence', methods=['OPTIONS'])
def options_sequence():
    url = request.json.get('url')
    return find_model(url=url)


@app.route('/sequence', methods=['POST'])
def play_sequence():
    url = request.json.get('url')
    user = request.json.get('user')
    cookies = user['cookies']
    # Create driver for this request
    driver = SeleniumDriver()
    # Go to url
    driver.get(url)
    # Add cookies to driver
    for cookie in cookies:
        cookie = {'name': cookie['name'], 'value': cookie['value']}
        driver.add_cookie(cookie)
    # Init Sequence
    sequence = Sequence(url=url, driver=driver)
    # play Sequence
    sequence.play()
    # get data from Sequence
    data = sequence.data
    return data


if __name__ == '__main__':
    app.run()
