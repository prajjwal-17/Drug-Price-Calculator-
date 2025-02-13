import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, jsonify, url_for , flash , render_template_string
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import csv
import pandas as pd

app = Flask(__name__)

load_dotenv()

app.secret_key = os.getenv("SECRET_KEY")

db_config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME")
}
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect if not logged in
db = mysql.connector.connect(**db_config)
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

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read the uploaded Excel file
        df = pd.read_excel(file)

        # Convert DataFrame to a list of dictionaries
        data = df.to_dict(orient='records')

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/')
def home():
    if 'user_id' in session and session.get('user_id') is not None:
        # Load data from the CSVs
        news = load_csv_data('data/pharmaceutical_news.csv')  # News articles
        reports = load_csv_data('data/medicine_demand.csv')  # Trending reports
        return render_template('home.html', news=news, reports=reports)
    
    session.clear()  # Ensure session is cleared for new visitors
    return redirect(url_for('login'))  # Redirect to login if not logged in


# Routes for other pages
@app.route('/calculator')
@login_required
def calculator():
    return render_template('calculator.html')

@app.route('/customers')
@login_required
def customers():
    return render_template('customers.html')

@app.route('/sales')
@login_required
def sales():
    return render_template('sales.html')

@app.route('/pricing', methods=['GET', 'POST'])
@login_required
def pricing():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        queries = request.json.get('queries', [])
        query_result = []

        try:
            # Apply queries based on user selection
            for query in queries:
                if query == "query1":
                    cursor.execute("""
                        SELECT * FROM medical2
                        WHERE `Industry Selling Price` < `Government Ceiling Price`
                    """)
                elif query == "query2":
                    cursor.execute("""
                        SELECT * FROM medical2
                        WHERE `Demand Level` = 'High'
                        AND `Industry Selling Price` = `Government Ceiling Price`
                    """)
                elif query == "query3":
                    cursor.execute("""
                        UPDATE medical2
                        SET `Industry Selling Price` = `Industry Selling Price` * 0.5
                        WHERE `Quantity Sold` > 50
                    """)

                
                elif query == "query4":
                    cursor.execute("""
                        SELECT *
                        FROM medical2
                        ORDER BY `Discount` DESC
                        ;
                    """)
                    query_result.extend(cursor.fetchall())
                elif query == "query5":
                    cursor.execute("""
                        SELECT *
                        FROM medical2
                        ORDER BY `Discount`
                        
                    """)
                    query_result.extend(cursor.fetchall())
                    
                elif query == "query6":
                    cursor.execute("""
                        SELECT * FROM medical2 WHERE `Demand Level` = 'low' AND `Price per Unit` >0.80 """)
                query_result.extend(cursor.fetchall())
                
                



                conn.commit()
                cursor.execute("SELECT * FROM medical2")  # Fetch updated data
                query_result.extend(cursor.fetchall())
            return jsonify(query_result)

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": str(e)}), 500

        finally:
            conn.close()

    # Default: Show the original table
    try:
        cursor.execute("SELECT * FROM medical")
        dataset = cursor.fetchall()
        conn.close()
        return render_template('pricing.html', dataset=dataset)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error=str(e))  # Provide an error template

@app.route('/AboutUs')
@login_required
def changelog():
    return render_template('about_us.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            return render_template_string("""
                <script>
                    alert("Passwords do not match!");
                    window.location.href = "/signup";
                </script>
            """)
            


        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                           (name, email, hashed_pw))
            db.commit()
            flash("Signup successful! You can now login.", "success")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return render_template_string(f"""
                <script>
                    alert("Error: {err}");
                    window.location.href = "/signup";
                </script>
            """)


    return render_template('Signup.html')


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
            return redirect(url_for('home'))
        else:
            return "Invalid Credentials"
            return redirect(url_for('login'))

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
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)