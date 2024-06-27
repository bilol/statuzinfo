from flask import Flask, render_template, redirect, url_for, flash
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/companies')
def companies_list():
    try:
        file_path = 'data.xlsx'
        df = pd.read_excel(file_path)
        companies = df.to_dict(orient='records')
        return render_template('companies.html', companies=companies)
    except Exception as e:
        print(f"Error reading data from Excel file: {e}")
        return render_template('companies.html', companies=[])

@app.route('/company/<int:company_id>')
def company_detail(company_id):
    try:
        file_path = 'data.xlsx'
        df = pd.read_excel(file_path)
        if company_id < len(df):
            company = df.iloc[company_id].to_dict()
            return render_template('company.html', company=company)
        else:
            flash('Company not found', 'danger')
            return redirect(url_for('companies_list'))
    except Exception as e:
        print(f"Error reading data from Excel file: {e}")
        return render_template('company.html', company=None)

@app.route('/partnerships')
def partnerships():
    return render_template('partnerships.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
