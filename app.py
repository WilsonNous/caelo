import os
import mysql.connector
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "caelo_secret_dev")


# =========================
# CONEXÃO MYSQL
# =========================
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        autocommit=True
    )


# =========================
# ROTAS PÚBLICAS
# =========================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/lead", methods=["POST"])
def salvar_lead():
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    email = request.form.get("email")
    mensagem = request.form["mensagem"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO leads (nome, telefone, email, mensagem, origem)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, telefone, email, mensagem, "Portal CAELO"))

    cur.close()
    conn.close()

    flash("Mensagem enviada com sucesso! Entraremos em contato.", "success")
    return redirect("/#contato")


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT * FROM users
            WHERE email = %s AND ativo = 1
        """, (email,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user and check_password_hash(user["senha"], senha):
            session["user_id"] = user["id"]
            session["tipo"] = user["tipo"]
            return redirect("/dashboard")

        flash("E-mail ou senha inválidos", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================
# ÁREA DO CLIENTE
# =========================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT * FROM documentos
        WHERE user_id = %s
        ORDER BY criado_em DESC
    """, (session["user_id"],))

    documentos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("dashboard.html", documentos=documentos)


# =========================
# ADMIN - LEADS
# =========================
@app.route("/admin/leads")
def admin_leads():
    if session.get("tipo") != "admin":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT * FROM leads
        ORDER BY criado_em DESC
    """)
    leads = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("admin_leads.html", leads=leads)


# =========================
if __name__ == "__main__":
    app.run(debug=True)
