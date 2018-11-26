"""
Create an endpoint/url website to store fb messenger input/output
Run this directly from the console!
"""

from flask import Flask, request

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
