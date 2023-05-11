from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "gamign"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=2)

db = SQLAlchemy(app)

# define the DB structure
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/meny")
def meny():
    return render_template("meny.html")

@app.route("/create", methods=["POST", "GET"])
def create():

    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        session["user"] = username

        found_user_username = users.query.filter_by(name=username).first()
        found_user_email = users.query.filter_by(email=email).first()

        if found_user_username:
            flash("Username already exists")
        elif found_user_email:
            flash("Email already exists")
        else:
            # Adding user data to the database
            new_user = users(username, email, password)
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully")

        return redirect(url_for("view"))
    else:
        # Check if account already exists
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("home"))

        return render_template("create.html")
    

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]
        
        user = users.query.filter_by(name=username).first()

        if user and user.password:
            session["user"] = user.name
            flash("Login successful")
            return redirect(url_for("user"))
        else:
            flash("Invalid username or password")

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
        return redirect(url_for("login"))
    else:
        session.pop("user", None)
        session.pop("email", None)
        return redirect(url_for("home"))

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email Saved")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in", "info")
        return redirect(url_for("login"))

@app.route("/view")
def view():
    all_users = users.query.all()
    return render_template("view.html", users=all_users)


@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/admin/deleteusers")
def delete_users():
    users.query.delete()
    db.session.commit()
    flash("All user data has been deleted")
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run()