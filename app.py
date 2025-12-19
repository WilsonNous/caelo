import os
import mysql.connector
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        connection_timeout=10,
        autocommit=True
    )


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

    flash("Mensagem enviada com sucesso! Entraremos em contato.", "success")
    return redirect("/#contato")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT * FROM users
            WHERE email = %s AND ativo = 1
        """, (request.form["email"],))

        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user["senha"], request.form["senha"]):
            session["user_id"] = user["id"]
            session["tipo"] = user["tipo"]
            return redirect("/dashboard")

        flash("E-mail ou senha inválidos", "error")

    return render_template("login.html")
