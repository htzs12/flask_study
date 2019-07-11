from flask import Flask, request, make_response, redirect


app = Flask(__name__)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>your browser is {0}</p>'.format(user_agent)


def name():
    return 'hello world'


app.add_url_rule('/name', 'name', name)


@app.route('/user/<name>')
def user(name):
    return 'hello {0}'.format(name)


@app.route('/requests')
def requests():
    return '{0}'.format(request.url)


@app.route('/error')
def errors():
    return 'bad request', 404


@app.route('/response')
def responses():
    response = make_response('<h1>This document carries a cookie!</h1>')
    # response.set_cookie('answer', 42)
    response.status_code
    return response
