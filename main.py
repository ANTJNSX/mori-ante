from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "gamign"
app.permanent_session_lifetime = timedelta(days=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/meny")
def meny():
    return render_template("meny.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        session["user"] = user
        flash("Login succesfull")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("home"))
        return render_template("login.html")

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("You have been logged out", "info")
        session.pop("user", None)
        return render_template("login.html")
    else:
        session.pop("user", None)
        return redirect(url_for("home"))

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in", "info")
        return redirect(url_for("login"))

@app.route("/menu")
def menu():
    return render_template("menu.html")

if __name__ == "__main__":
    app.run()

