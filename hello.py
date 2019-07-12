from flask import Flask, request, make_response, redirect, render_template, url_for

from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app11)


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
    return response


@app.route('/redirect')
def redict():
    return redirect('https://www.baidu.com')


@app.route('/jinja')
def jinja():
    return render_template('index.html', name='浩哥哥')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


