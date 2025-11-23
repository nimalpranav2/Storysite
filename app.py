from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)
PASSWORD = "mod123"

# --- Database setup ---
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        part TEXT,
        story TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html", password=PASSWORD)

    if request.form.get("password") != PASSWORD:
        return "Wrong password"

    name = request.form.get("name")
    part = request.form.get("part")
    story = request.form.get("story")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO stories (name, part, story) VALUES (?, ?, ?)", (name, part, story))
    conn.commit()
    conn.close()

    return redirect("/list")

@app.route("/list")
def list_stories():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM stories")
    data = c.fetchall()
    conn.close()
    return render_template("list.html", stories=data)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        story_id = request.args.get("id")
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT story FROM stories WHERE id=?", (story_id,))
        story = c.fetchone()[0]
        conn.close()
        return render_template("edit.html", id=story_id, story=story, password=PASSWORD)

    if request.form.get("password") != PASSWORD:
        return "Wrong password"

    story_id = request.form.get("id")
    new_story = request.form.get("story")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE stories SET story=? WHERE id=?", (new_story, story_id))
    conn.commit()
    conn.close()

    return redirect("/list")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
