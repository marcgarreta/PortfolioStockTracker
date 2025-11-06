from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3
import yfinance as yf
from werkzeug.security import generate_password_hash, check_password_hash
from models import init_db

# Config app
app = Flask(__name__)
app.secret_key = 'Hola123'

# Db helper function
def get_db():
    conn = sqlite3.connect('investment.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Register 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        conn = get_db()

        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                     (username, generate_password_hash(password)))
        conn.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = get_db()

    investments = conn.execute("SELECT * FROM investments WHERE user_id = ?", (user_id,)).fetchall()
    portfolio = []
    total_value, total_cost = 0.0, 0.0

    for inv in investments:
        try: 
            # Fetch live price using yfinance
            ticker = yf.Ticker(inv['symbol'])
            live_price = ticker.history(period='1d')['Close'].iloc[-1]
        except Exception:
            live_price = 0.0 # Fallback in case of error -- if symbol is invalid

        current_value = inv['quantity'] * live_price
        cost = inv['quantity'] * inv['buy_price']

        total_value += current_value
        total_cost += cost

        portfolio.append({
            'id': inv['id'],
            'symbol': inv['symbol'],
            'category': inv['category'],
            'quantity': inv['quantity'],
            'buy_price': inv['buy_price'],
            'current_price': round(live_price, 2),
            'value': round(current_value, 2),
            'profit_loss': round(current_value - cost, 2)
        })

    profit_loss = total_value - total_cost
    return render_template('dashboard.html', 
                           investments=portfolio, 
                           total_value=round(total_value,2), 
                           total_cost=round(total_cost,2), 
                           profit_loss=round(profit_loss,2),
)

# Add Investment
@app.route('/add_investment', methods=['GET', 'POST'])
def add_investment():
    if "user_id" not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        symbol = request.form['symbol']
        category = request.form['category']
        quantity = float(request.form['quantity'])
        buy_price = float(request.form['buy_price'])

        conn = get_db()
        conn.execute('''INSERT INTO investments (user_id, symbol, category, quantity, buy_price) 
                        VALUES (?, ?, ?, ?, ?)''', 
                     (session["user_id"], symbol, category, quantity, buy_price))
        conn.commit()
        flash('Investment added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_investment.html')

# Delete Investment
@app.route('/delete/<int:inv_id>')
def delete_investment(inv_id):
    if "user_id" not in session:
        return redirect(url_for('login'))

    conn = get_db()
    conn.execute("DELETE FROM investments WHERE id = ? AND user_id = ?", (inv_id, session["user_id"]))
    conn.commit()
    flash('Investment deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# Edit Investment
@app.route('/edit/<int:inv_id>', methods=['GET', 'POST'])
def edit_investment(inv_id):
    if "user_id" not in session:
        return redirect(url_for('login'))

    conn = get_db()

    if request.method == "POST":
        quantity = float(request.form['quantity'])
        buy_price = float(request.form['buy_price'])

        conn.execute('UPDATE investments SET quantity=?, buy_price=? WHERE id=?',
                        (quantity, buy_price, inv_id))
        conn.commit()
        flash('Investment updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    investment = conn.execute("SELECT * FROM investments WHERE id = ? AND user_id = ?", 
                              (inv_id, session["user_id"])).fetchone()
    return render_template('edit_investment.html', investment=investment)

# Execute the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
