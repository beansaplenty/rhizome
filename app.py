from flask import Flask, render_template, request, redirect, url_for
import os
import re

app = Flask(__name__)
DATA_DIR = "pages"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# --- Helper functions ---
def get_page_content(title):
    path = os.path.join(DATA_DIR, f"{title}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_page_content(title, content):
    path = os.path.join(DATA_DIR, f"{title}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def get_all_pages():
    return sorted([f[:-4] for f in os.listdir(DATA_DIR) if f.endswith(".txt")])

def auto_link_content(content):
    pages = get_all_pages()
    def replace_word(match):
        word = match.group(0)
        if word in pages:
            return f'<a href="/wiki/{word}">{word.replace("_", " ")}</a>'
        return word
    return re.sub(r'\b\w[\w_]*\b', replace_word, content)

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        new_title = request.form.get("new_title").replace(" ", "_")
        save_page_content(new_title, "New page content here...")
        return redirect(url_for("edit", title=new_title))
    pages = get_all_pages()
    return render_template("index.html", pages=pages)

@app.route("/wiki/<title>")
def page(title):
    raw_content = get_page_content(title)
    content = auto_link_content(raw_content)
    links = [p for p in get_all_pages() if p != title]
    return render_template("page.html", title=title, content=content, links=links)

@app.route("/edit/<title>", methods=["GET", "POST"])
def edit(title):
    if request.method == "POST":
        content = request.form["content"]
        save_page_content(title, content)
        return redirect(url_for("page", title=title))
    content = get_page_content(title)
    return render_template("edit.html", title=title, content=content)

# --- Render-ready run ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
