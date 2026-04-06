from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shreshta7",
        database="todo_app"
    )

@app.route('/')
def home():
    return redirect('/login')

# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                    (request.form['username'], request.form['password']))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect('/dashboard')

    return render_template('login.html')

# REGISTER
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (username,password) VALUES (%s,%s)",
            (request.form['username'], request.form['password'])
        )

        conn.commit()
        conn.close()

        return redirect('/login')   # 🔥 THIS IS KEY

    return render_template('register.html')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT username FROM users WHERE id=%s", (session['user_id'],))
    username = cur.fetchone()[0]

    cur.execute("SELECT * FROM tasks WHERE user_id=%s", (session['user_id'],))
    tasks = cur.fetchall()

    conn.close()

    return render_template('dashboard.html', tasks=tasks, username=username)

# PROFILE
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT username FROM users WHERE id=%s", (session['user_id'],))
    username = cur.fetchone()[0]

    conn.close()

    return render_template('profile.html', username=username)

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# TASK APIs
@app.route('/add', methods=['POST'])
def add():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO tasks (user_id,task,deadline) VALUES (%s,%s,%s)",
                (session['user_id'], request.form['task'], request.form['deadline']))

    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT status FROM tasks WHERE id=%s", (id,))
    status = cur.fetchone()[0]
    new = 1 if status == 0 else 0

    cur.execute("UPDATE tasks SET status=%s WHERE id=%s", (new, id))
    conn.commit()
    conn.close()

    return jsonify({"status": new})

app.run(debug=True)