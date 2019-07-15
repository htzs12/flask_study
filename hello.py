import os
from datetime import datetime

from flask import Flask, request, make_response, redirect, render_template, url_for, session, flash

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class NameForm(FlaskForm):
    name = StringField('wath is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __str__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __str__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    name = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        # old_name = session.get('name')
        # if old_name is not None and old_name != form.name.data:
        #     flash('两次输入的值不一致，请重新输读入~')
        # session['name'] = form.name.data
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form, name=session.get('name'),
                           known=session.get('known', False)
                           )


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
@app.route('/jinja1')
def jinja():
    return render_template('index.html', name='浩哥哥')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
