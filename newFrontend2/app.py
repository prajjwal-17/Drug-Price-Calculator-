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
    news = load_csv_data('static/data/pharmaceutical_news.csv')  # Updated path
    reports = load_csv_data('static/data/medicine_demand.csv')  # Updated path
    return render_template('home.html', news=news, reports=reports)

# Routes for other pages
@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/customers')
def customers():
    return render_template('customers.html')

@app.route('/company')
def company():
    return render_template('company.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/login')  # Added missing login route
def login():
    return render_template('login.html')

@app.route('/signup')  # Added missing signup route
def signup():
    return render_template('signup.html')

if __name__ == '__main__':  # Fixed incorrect `__name__`
    app.run(debug=True)
