from flask import Flask, request, render_template, redirect, url_for, render_template_string
import mysql.connector

app = Flask(__name__)

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # Update if different
    database="project"
)
cursor = conn.cursor()

# 🏠 Expense Form (Home Page)
@app.route('/')
def form():
    cursor.execute("SELECT user_id, username FROM users")
    users = cursor.fetchall()
    return render_template('add_expense.html', users=users)

# ✅ Handle Expense Submission
@app.route('/submit', methods=['POST'])
def submit():
    amount = request.form['amount']
    date = request.form['date']
    description = request.form['description']
    category_id = request.form['category_id']
    method_id = request.form['method_id']
    user_id = request.form['user_id']

    # Ensure user exists
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
    if not cursor.fetchone():
        return "❌ Error: User ID does not exist."

    # Insert expense
    sql = '''
        INSERT INTO expenses (amount, expense_date, description, category_id, method_id, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    values = (amount, date, description, category_id, method_id, user_id)
    cursor.execute(sql, values)
    conn.commit()

    return redirect(url_for('form'))

# 👤 Register User
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return "❌ Username already exists. Try another one."

        # Insert user (user_id will auto-increment)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        conn.commit()
        user_id = cursor.lastrowid  # get the assigned user_id

        return f"✅ Registration successful! Your User ID is <b>{user_id}</b>. You can now use this ID to add expenses."

    return render_template('register.html')

# 👥 View All Users (optional)
@app.route('/users')
def show_users():
    cursor.execute("SELECT user_id, username FROM users")
    users = cursor.fetchall()
    return render_template_string("""
    <h2>Registered Users</h2>
    <ul>
      {% for user in users %}
        <li>User ID: {{ user[0] }}, Username: {{ user[1] }}</li>
      {% endfor %}
    </ul>
    """, users=users)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
