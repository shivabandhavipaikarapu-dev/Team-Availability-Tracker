from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

# Database connection
conn = sqlite3.connect("team.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS team (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    available INTEGER
)
""")

# Insert default members once
cursor.execute("SELECT * FROM team")
data = cursor.fetchall()

if len(data) == 0:
    members = [
        ("Aarav", 1),
        ("Riya", 0),
        ("gaurav", 1)
    ]

    cursor.executemany("INSERT INTO team (name, available) VALUES (?, ?)", members)
    conn.commit()


@app.route("/")
def home():
    cursor.execute("SELECT * FROM team")
    members = cursor.fetchall()

    return render_template("index.html", members=members)


@app.route("/toggle/<int:id>")
def toggle(id):
    cursor.execute("SELECT available FROM team WHERE id=?", (id,))
    current = cursor.fetchone()[0]

    new_status = 0 if current == 1 else 1

    cursor.execute("UPDATE team SET available=? WHERE id=?", (new_status, id))
    conn.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)