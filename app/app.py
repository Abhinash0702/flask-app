
# app/app.py
from flask import Flask, request, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

# Flag: skip DB in CI/demo mode when SKIP_DB=1
SKIP_DB = os.environ.get('SKIP_DB') == '1'

db_config = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'root'),
    'database': os.environ.get('DB_NAME', 'usersdb')
}

def init_db_if_needed():
    """Create table only when DB is enabled."""
    if SKIP_DB:
        return
    # In real envs you might want to wait for DB
    time.sleep(10)
    conn = mysql.connector.connect(**db_config)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        ''')
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Initialize DB only if not skipping
init_db_if_needed()

@app.route('/', methods=['GET'])
def addusers_form():
    return '''
        <h2>Add User</h2>
        /submituser
            Name: <input type="text" name="name"><br><br>
            Email: <input type="email" name="email"><br><br>
            <input type="submit" value="Add User">
        </form>
    '''

@app.route('/submituser', methods=['POST'])
def submit_user():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()

    if SKIP_DB:
        # Demo/CI mode: do not hit DB
        return f'<p>Demo mode: User {name} would be added!</p>/Add another</a>'

    conn = mysql.connector.connect(**db_config)
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    return f'<p>User {name} added successfully!</p>/Add another</a>'

@app.route('/users', methods=['GET'])
def get_users():
    if SKIP_DB:
        # Demo/CI mode: return empty list
        return jsonify([])

    conn = mysql.connector.connect(**db_config)
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email FROM users')
        users = [{"id": row[0], "name": row[1], "email": row[2]} for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()

    return jsonify(users)

if __name__ == '__main__':
    # Only for local dev runs; in production use a WSGI server
    app.run(host='0.0.0.0', port=5000)
