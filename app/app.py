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


def init_db_if_needed(max_retries: int = 12, backoff_seconds: int = 5):
    """Create table only when DB is enabled. Wait/retry for DB readiness."""
    if SKIP_DB:
        return

    attempt = 0
    while attempt < max_retries:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100)
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
            return
        except mysql.connector.Error as e:
            attempt += 1
            print(f"DB not ready (attempt {attempt}/{max_retries}): {e}")
            time.sleep(backoff_seconds)

    raise RuntimeError("Database not reachable after retries; aborting app start.")


# Initialize DB only if not skipping
init_db_if_needed()



@app.route('/', methods=['GET'])
def addusers_form():
    return '''
        <h2>Add User</h2>
        <form method="post" action="/submituser">
            Name: <input type="text" name="name"><br><br>
            Email: <input type="email" name="email"><br><br>
            <input type="submit" value="Add User">
        </form>
    '''

@app.route('/submituser', methods=['POST'])
def submit_user():
    name = request.form['name']
    email = request.form['email']
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    return f'<p>User {name} added successfully!</p><a href="/">Add another</a>'

@app.route('/users', methods=['GET'])
def get_users():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email FROM users')
    users = [{"id": row[0], "name": row[1], "email": row[2]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
