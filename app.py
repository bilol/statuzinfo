import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask import Flask, render_template, redirect, url_for, flash, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError, OperationalError
import pandas as pd
from config import config

app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIG', 'default')
app.config.from_object(config[config_name])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    subscription = db.Column(db.String(100), nullable=True)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            flash('Username or email already exists', 'danger')
            print(f"IntegrityError: {e}")
        except OperationalError as e:
            db.session.rollback()
            flash('Database connection error. Please try again later.', 'danger')
            print(f"OperationalError: {e}")
        except Exception as e:
            db.session.rollback()
            flash('An unexpected error occurred. Please try again.', 'danger')
            print(f"Unexpected error: {e}")
    else:
        print("Form errors:", form.errors)
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/')
def index():
    return render_template('index.html', title=current_app.config['APP_NAME'])

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/team')
def team():
    return render_template('team.html', title='Team')

@app.route('/companies')
def companies_list():
    try:
        file_path = current_app.config['DATA_FILE_PATH']
        df = pd.read_excel(file_path)
        companies = df.to_dict(orient='records')
        return render_template('companies.html', companies=companies, title='Companies')
    except Exception as e:
        print(f"Error reading data from Excel file: {e}")
        return render_template('companies.html', companies=[], title='Companies')

@app.route('/partnerships')
def partnerships():
    return render_template('partnerships.html', title='Partnerships')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', title='Pricing')

@app.route('/company/<int:company_id>')
def company_detail(company_id):
    try:
        file_path = current_app.config['DATA_FILE_PATH']
        df = pd.read_excel(file_path)
        if company_id < len(df):
            company = df.iloc[company_id].to_dict()
            return render_template('company.html', company=company, title='Company Detail')
        else:
            flash('Company not found', 'danger')
            return redirect(url_for('companies_list'))
    except Exception as e:
        print(f"Error reading data from Excel file: {e}")
        flash('An error occurred while retrieving the company details.', 'danger')
        return redirect(url_for('companies_list'))

@app.context_processor
def inject_app_name():
    return dict(APP_NAME=current_app.config['APP_NAME'])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)