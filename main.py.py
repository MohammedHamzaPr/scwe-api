from flask import Flask, request, jsonify
import sqlite3 as sql
import os
app = Flask(__name__)

connect = sql.connect('data.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users(username TEXT, 
                password TEXT,
                mail TEXT,
                date TEXT)''')
connect.commit()
cursor.close()

@app.route('/check_username', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data['username']
    cursor = connect.cursor()
    avalible = "avalible" if cursor.execute('SELECT username FROM users WHERE username=?',(username,)).fetchone() == None else "not avalible"
    return avalible

# هنا نقوم بأضافة مستخدم جديد الى قاعدة البيانات
@app.route('/add_user', methods=['POST'])
def add_user():
    cursor = connect.cursor()
    data = request.get_json()
    cursor.execute(f'CREATE TABLE {data["username"]}(id TEXT, account TEXT, username TEXT, mail TEXT,password TEXT,phone TEXT, url TEXT)')
    cursor.execute('INSERT INTO users VALUES(?,?,?,?)',(data['username'],data['password'],data['mail'],data['date']))
    connect.commit()
    cursor.close()
    return "Data added succfily"

@app.route('/check_server', methods=['GET'])
def check_server():
    return "running"

@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.get_json()
    cursor = connect.cursor()
    cursor.execute(f'DELETE FROM {data["username"]}')
    username = data['username']
    for i in data['data']:
        cursor.execute(f'INSERT INTO {username} VALUES(?,?,?,?,?,?,?)', i)
    connect.commit()
    cursor.close()
    return "work"

@app.route('/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    cursor = connect.cursor()
    username = data['username']
    cursor.execute(f'SELECT * FROM {username}')
    return jsonify({'data':cursor.fetchall()})

# هنا نقوم بأضافة مستخدم جديد الى قاعدة البيانات
@app.route('/remove_data', methods=['POST'])
def remove_data():
    cursor = connect.cursor()
    data = request.get_json()
    cursor.execute(f'DELETE FROM {data["username"]} where id=?',(data["uid"], ))
    connect.commit()
    cursor.close()
    return "Data was deleted"

# هنا نقوم بأضافة معلومات جديدة الى المستخدم
@app.route('/add_new_data', methods=['POST'])
def add_new_data():
    cursor = connect.cursor()
    data = request.get_json()
    values = [data['id'], data['account'], data['username'], data['mail'], data['password'], data['phone'], data['url']]

    tables = [tuble[0] for tuble in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    if data['table'] in tables:
        cursor.execute(f'''
        INSERT INTO {data['table']} VALUES(
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?)''',values)
        connect.commit()
        cursor.close()
        return f"Done added the new data"
    else: return "Cannot add the values :("


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
