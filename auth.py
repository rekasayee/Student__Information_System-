from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import db

auth = Blueprint('auth', __name__)

# ---------------------- REGISTER ----------------------
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        role = request.form["role"]

        # Prevent empty input
        if not username or not password:
            flash("Username and password cannot be empty.", "danger")
            return redirect(url_for("auth.register"))

        # Hash password
        hashed = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed, role)
            )
            flash("User registered successfully!", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash("Username already exists.", "danger")

    return render_template("register.html")


# ---------------------- LOGIN ----------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        # Fetch user
        user = db.query("SELECT * FROM users WHERE username=?", (username,), one=True)

        if not user:
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))

        stored_hash = user["password"]

        # Validate password
        if check_password_hash(stored_hash, password):
            session["user"] = user["username"]
            session["role"] = user["role"]
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


# ---------------------- LOGOUT ----------------------
@auth.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))
