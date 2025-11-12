from flask import Flask, render_template, request, redirect, url_for
import sqlite3, re, os

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("wiki.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    db = get_db()
    pages = db.execute("SELECT title FROM pages").fetchall()
    return render_template("index.html", pages=pages)

@app.route("/wiki/<title>")
def view_page(title):
    db = get_db()
    page = db.execute("SELECT * FROM pages WHERE title=?", (title,)).fetchone()
    if not page:
        return redirect(url_for("edit_page", title=title))
    # Turn [[PageName]] into clickable links
    content = re.sub(r"\[\[(.*?)\]\]", r'<a href="/wiki/\1">\1</a>', page["content"])
    return render_template("page.html", title=title, content=content)

@app.route("/edit/<title>", methods=["GET", "POST"])
def edit_page(title):
    db = get_db()
    if request.method == "POST":
        content = request.form["content"]
        db.execute("REPLACE INTO pages (title, content) VALUES (?, ?)", (title, content))
        db.commit()
        return redirect(url_for("view_page", title=title))
    page = db.execute("SELECT * FROM pages WHERE title=?", (title,)).fetchone()
    return render_template("edit.html", title=title, content=page["content"] if page else "")

# Create database if it doesn’t exist
if not os.path.exists("wiki.db"):
    db = sqlite3.connect("wiki.db")
    db.execute("CREATE TABLE pages (title TEXT PRIMARY KEY, content TEXT)")
    db.commit()
    db.close()

if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

