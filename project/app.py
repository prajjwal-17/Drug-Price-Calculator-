import csv
from flask import Flask, render_template

app = Flask(__name__)

# Function to load CSV data
def load_csv_data(filepath):
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"File {filepath} not found. Ensure the script has been run to generate the data.")
    return data

@app.route('/')
def home():
    # Load data from the CSVs
    news = load_csv_data('data/pharmaceutical_news.csv')  # News articles
    reports = load_csv_data('data/medicine_demand.csv')  # Trending reports
    return render_template('home.html', news=news, reports=reports)

# Routes for other pages
@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/customers')
def customers():
    return render_template('customers.html')

@app.route('/sales')
def sales():
    return render_template('sales.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/AboutUs')
def changelog():
    return render_template('about_us.html')

@app.route('/login')  # Added missing login route
def login():
    return render_template('login.html')

@app.route('/signup')  # Added missing signup route
def signup():
    return render_template('signup.html')
if __name__ == '__main__':
    app.run(debug=True)
