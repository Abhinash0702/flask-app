from flask import Flask, request, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

# Wait for MySQL to be ready
time.sleep(10)

db_config = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'root'),
    'database': os.environ.get('DB_NAME', 'usersdb')
}

# Create table if not exists
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
