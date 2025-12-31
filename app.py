import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# -----------------------------
# Database connection function
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect("student_feedback.db")
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# Login page
# -----------------------------
@app.route("/")
def login():
    return render_template("login.html")

# -----------------------------
# Student page
# -----------------------------
@app.route("/student")
def student():
    return render_template("index.html")

# -----------------------------
# Submit feedback
# -----------------------------
@app.route("/submit", methods=["POST"])
def submit_feedback():

    department = request.form["department"]
    subject = request.form["subject"]
    faculty = request.form["faculty"]
    rating = request.form["rating"]
    message = request.form["message"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (department, subject, faculty, rating, message)
        VALUES (?, ?, ?, ?, ?)
    """, (department, subject, faculty, rating, message))

    conn.commit()
    conn.close()

    return redirect("/student")

# -----------------------------
# Admin page
# -----------------------------
@app.route("/admin")
def admin():
    conn = get_db_connection()
    feedbacks = conn.execute("SELECT * FROM feedback").fetchall()
    conn.close()
    return render_template("admin.html", feedbacks=feedbacks)

# -----------------------------
# Faculty page
# -----------------------------
@app.route("/faculty")
def faculty():
    conn = get_db_connection()
    feedbacks = conn.execute("SELECT * FROM feedback").fetchall()
    conn.close()
    return render_template("faculty.html", feedbacks=feedbacks)

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
