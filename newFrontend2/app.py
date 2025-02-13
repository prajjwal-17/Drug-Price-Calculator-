from flask import Flask, render_template, request, redirect, session, jsonify, url_for, flash
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
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
    return data

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",              # Change this
    password="pawnstar1234",    # Change this
    database="test"           # Your database name
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
    news = load_csv_data('data/pharmaceutical_news.csv')
    reports = load_csv_data('data/medicine_demand.csv')
    return render_template('home.html', news=news, reports=reports, user=current_user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('signup'))
        
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                           (name, email, hashed_pw))
            db.commit()
            flash("Account created! Please log in.", "success")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "error")
            return redirect(url_for('signup'))

    return render_template('signup.html', user=current_user)

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
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid Credentials", "error")
            return redirect(url_for('login'))

    return render_template('login.html', user=current_user)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('home'))


@app.route('/calculator')
def calculator():
    return render_template('calculator.html', user=current_user)

@app.route('/customers')
def customers():
    return render_template('customers.html', user=current_user)

@app.route('/sales')
def sales():
    return render_template('sales.html', user=current_user)

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
        return render_template('pricing.html', dataset=dataset, user=current_user)
    except Exception as e:
        return render_template('error.html', error=str(e), user=current_user)

@app.route('/AboutUs')
def about_us():
    return render_template('about_us.html', user=current_user)

if __name__ == "__main__":
    app.run(debug=True)
