from flask import Flask, request
from selenium_sequence import Automnation, find_model

app = Flask(__name__)


@app.route('/model', methods=['POST'])
def get_url_model():
    url = request.json.get('url')
    return find_model(url=url)


@app.route('/automnation/play', methods=['POST'])
def play_sequence() -> dict:
    automnation = Automnation(
        # urls=url, 
        #  auth=auth, 
        #  filename=filename, 
        headless=True,
        _id=request.json.get('_id'))
    return automnation.play()


if __name__ == '__main__':
    app.run()
