from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "secret123"

# DB CONNECTION
def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT")),
        connection_timeout=5
    )

# HOME
@app.route('/')
def home():
    return redirect('/login')


# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (request.form['username'], request.form['password'])
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect('/dashboard')
        else:
            error = "Invalid credentials ❌"

    return render_template('login.html', error=error)


# REGISTER
@app.route('/register', methods=['GET','POST'])
def register():
    error = None

    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()

        # check if user exists
        cur.execute("SELECT * FROM users WHERE username=%s", (request.form['username'],))
        existing = cur.fetchone()

        if existing:
            error = "User already exists ⚠️"
        else:
            cur.execute(
                "INSERT INTO users (username,password) VALUES (%s,%s)",
                (request.form['username'], request.form['password'])
            )
            conn.commit()
            conn.close()
            return redirect('/login')

        conn.close()

    return render_template('register.html', error=error)


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


#ADD TASK
@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (user_id, task, deadline) VALUES (%s,%s,%s)",
        (session['user_id'], request.form['task'], request.form['deadline'])
    )

    conn.commit()
    conn.close()

    return jsonify({"ok": True})


# DELETE TASK
@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id=%s AND user_id=%s",
        (id, session['user_id'])
    )

    conn.commit()
    conn.close()

    return jsonify({"ok": True})


# TOGGLE COMPLETE
@app.route('/complete/<int:id>')
def complete(id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT status FROM tasks WHERE id=%s AND user_id=%s",
        (id, session['user_id'])
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    status = row[0]
    new_status = 1 if status == 0 else 0

    cur.execute(
        "UPDATE tasks SET status=%s WHERE id=%s AND user_id=%s",
        (new_status, id, session['user_id'])
    )

    conn.commit()
    conn.close()

    return jsonify({"status": new_status})


# RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
