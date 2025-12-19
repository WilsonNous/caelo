import os
import mysql.connector
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# =========================
# DATABASE
# =========================
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        autocommit=True
    )


# =========================
# AUTH DECORATOR
# =========================
def login_required(tipo=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect("/login")
            if tipo and session.get("tipo") != tipo:
                return redirect("/dashboard")
            return f(*args, **kwargs)
        return wrapper
    return decorator


# =========================
# PUBLIC
# =========================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/lead", methods=["POST"])
def salvar_lead():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO leads (nome, telefone, email, mensagem, origem)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        request.form["nome"],
        request.form["telefone"],
        request.form.get("email"),
        request.form["mensagem"],
        "Portal CAELO"
    ))

    cur.close()
    conn.close()

    flash("Mensagem enviada com sucesso!", "success")
    return redirect("/#contato")


# =========================
# LOGIN / LOGOUT
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            "SELECT * FROM users WHERE email=%s AND ativo=1",
            (request.form["email"],)
        )
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user and check_password_hash(user["senha"], request.form["senha"]):
            session["user_id"] = user["id"]
            session["tipo"] = user["tipo"]
            return redirect("/dashboard")

        flash("Login inválido", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
@login_required()
def dashboard():
    return render_template("dashboard.html")


# =========================
if __name__ == "__main__":
    app.run(debug=True)
