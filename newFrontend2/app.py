from flask import Flask, render_template, request, redirect, session, jsonify, url_for
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import csv

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for security

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
    return data  # Fixed indentation issue

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect if not logged in

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",   # Change this
    password="pawnstar1234",  # Change this
    database="test"  # Your database name
)
cursor = db.cursor(dictionary=True)

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return User(user['id'], user['name'], user['email'])
    return None

@app.route('/')
def home():
    # Load data from the CSVs
    news = load_csv_data('data/pharmaceutical_news.csv')  # News articles
    reports = load_csv_data('data/medicine_demand.csv')  # Trending reports
    return render_template('home.html', news=news, reports=reports)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        if password != confirm_password:
            return "Passwords do not match!"
        
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                           (name, email, hashed_pw))
            db.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['name'], user['email'])
            login_user(user_obj)
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials"

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome, {session['user_name']}! <br><a href='/logout'>Logout</a>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/customers')
def customers():
    return render_template('customers.html')

@app.route('/sales')
def sales():
    return render_template('sales.html')

@app.route('/pricing', methods=['GET', 'POST'])
def pricing():
    if request.method == 'POST':
        queries = request.json.get('queries', [])
        query_result = []

        try:
            for query in queries:
                if query == "query1":
                    cursor.execute("SELECT * FROM medicalfiltered WHERE Industry_Selling_Price < Government_Ceiling_Price")
                elif query == "query2":
                    cursor.execute("SELECT * FROM medicalfiltered WHERE Demand_Level = 'High' AND Industry_Selling_Price = Government_Ceiling_Price")
                elif query == "query3":
                    cursor.execute("UPDATE medicalfiltered SET Industry_Selling_Price = Industry_Selling_Price * 0.5 WHERE Quantity_Sold > 50")
                    db.commit()
                    cursor.execute("SELECT * FROM medicalfiltered")
                
                query_result.extend(cursor.fetchall())

            return jsonify(query_result)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    try:
        cursor.execute("SELECT * FROM medicalfiltered")
        dataset = cursor.fetchall()
        return render_template('pricing.html', dataset=dataset)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/AboutUs')
def about_us():
    return render_template('about_us.html')

if __name__ == "__main__":
    app.run(debug=True)
