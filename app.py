from flask import Flask, request, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
import csv
from typing import List, Dict

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

# -------------------------
# Flask-Login Setup
# -------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore  ← Fix for type-checkers like MyPy/Pyright

# Dummy User class
class User(UserMixin):
    def __init__(self, user_id: int):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id: str):
    try:
        return User(int(user_id))
    except ValueError:
        return None

# -------------------------
# In-memory Data
# -------------------------
cargo_list: List[Dict[str, float]] = []
max_weight: float = 1000.0
logs: List[str] = []

# -------------------------
# Routes
# -------------------------
@app.route('/')
@login_required
def home():
    total_weight = sum(item['weight'] for item in cargo_list)
    return render_template(
        'home.html',
        cargo_list=cargo_list,
        total_weight=total_weight,
        max_weight=max_weight
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if username == 'admin' and password == 'admin':
            user = User(1)
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid credentials.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
@login_required
def add():
    name = request.form.get('name', '').strip()
    weight_str = request.form.get('weight', '').strip()

    try:
        weight = float(weight_str)
        if weight <= 0:
            raise ValueError()
    except ValueError:
        flash('Weight must be a positive number.', 'error')
        return redirect(url_for('home'))

    total_weight = sum(item['weight'] for item in cargo_list) + weight

    if total_weight > max_weight:
        flash(f'Cannot add cargo. Total weight would exceed {max_weight} kg.', 'error')
    else:
        cargo = {'name': name, 'weight': weight}
        cargo_list.append(cargo)
        logs.append(f"Added cargo: {name}, {weight}kg")
        flash('Cargo added successfully!', 'success')

    return redirect(url_for('home'))

@app.route('/export')
@login_required
def export():
    try:
        with open('cargo.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Weight'])
            for item in cargo_list:
                writer.writerow([item['name'], item['weight']])
        flash('Exported as CSV successfully!', 'success')
    except Exception as e:
        flash(f"Error exporting file: {str(e)}", 'error')
    return redirect(url_for('home'))

# Optional route to view logs
@app.route('/logs')
@login_required
def view_logs():
    return render_template('logs.html', logs=logs)

# -------------------------
# App Entry Point
# -------------------------
if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, port=8000)

