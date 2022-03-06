import re
from datetime import timedelta
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    make_response,
)
from flask_sqlalchemy import SQLAlchemy

# from models import User, db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "HelloWorld"
app.permanent_session_lifetime = timedelta(minutes=10)
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80), unique=False, nullable=True)
    last = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __init__(self, first, last, email, password):
        self.first = first
        self.last = last
        self.email = email
        self.password = password


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80), unique=False, nullable=True)
    title = db.Column(db.String(80), unique=False, nullable=True)
    post = db.Column(db.String(80), unique=False, nullable=True)

    def __init__(self, first, title, post):
        self.first = first
        self.title = title
        self.post = post


@app.route("/")
def home():
    return render_template(
        "home.html",
        first=session["first"],
        last=session["last"],
        email=session["email"],
        admin=session["admin"],
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    msg = " "
    form = request.form
    remail = request.cookies.get("email")
    rpassword = request.cookies.get("password")
    radmin = request.cookies.get("admin")
    listfirst = []
    listlast = []
    listemail = []

    if remail and rpassword:
        if radmin == True:
            user = Users.query.all()
        else:
            user = list(Users.query.filter_by(email=remail, password=rpassword))
        session["email"] = remail
        session["password"] = rpassword
        session["admin"] = radmin
        for index in range(len(user)):
            listfirst.append(user[index].first)
            listlast.append(user[index].last)
            listemail.append(user[index].email)

        return redirect(
            url_for(
                "home", first=listfirst, last=listlast, email=listemail, admin=radmin
            )
        )

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        checked = "checkbox" in request.form

        if len(email) == 0:
            msg = "Please enter an email addresss"
        elif not re.match("[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid Email Address"
        elif len(password) == 0:
            msg = "Please enter a password"
        else:
            session["admin"] = False
            if email == "admin@gmail.com" and password == "password":
                session["admin"] = True
                user = Users.query.all()

            else:
                user = list(Users.query.filter_by(email=email, password=password))

            if user:
                for index in range(len(user)):
                    listfirst.append(user[index].first)
                    listlast.append(user[index].last)
                    listemail.append(user[index].email)
                session["currentemail"] = email
                session["password"] = password
                session["first"] = listfirst
                session["last"] = listlast
                session["email"] = listemail
                if checked:
                    return redirect(url_for("setcookie"))
                return redirect(
                    url_for(
                        "home",
                    )
                )
            else:
                msg = "Invalid Email address or password"
    return render_template("login.html", msg=msg, form=form)


@app.route("/setcookie", methods=["POST", "GET"])
def setcookie():
    cookie = make_response(redirect(url_for("home")))
    cookie.set_cookie("email", session["currentemail"])
    cookie.set_cookie("password", session["password"])
    cookie.set_cookie("admin", str(session["admin"]))
    return cookie


@app.route("/logout")
def logout():
    session["admin"] = False
    session["first"] = ""
    session["last"] = ""
    cookie = make_response(redirect(url_for("login")))
    cookie.set_cookie("email", "", expires=0)
    cookie.set_cookie("password", "", expires=0)

    return cookie


@app.route("/about")
def about():
    return render_template(
        "about.html",
        first=session["first"],
        last=session["last"],
        email=session["email"],
        admin=session["admin"],
    )


@app.route("/userlist")
def userList():
    output = []
    for i in range(len(session["first"])):
        output.append(
            {
                "first": session["first"][i],
                "last": session["last"][i],
                "email": session["email"][i],
            }
        )

    return render_template(
        "userlist.html",
        first=session["first"],
        last=session["last"],
        email=session["email"],
        admin=session["admin"],
        output=output,
    )


@app.route("/register", methods=["POST", "GET"])
def register():
    msg = " "
    form = request.form
    if request.method == "POST":
        first = request.form["fname"]
        last = request.form["lname"]
        email = request.form["email"]
        password = request.form["password"]
        rpassword = request.form["rpassword"]

        if len(first) == 0 or first.isdigit():
            msg = "Invalid First Name!"
        elif len(last) == 0 or last.isdigit():
            msg = "Invalid Last Name!"
        elif len(email) == 0:
            msg = "Please enter an email addresss"
        elif not re.match("[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid Email Address"
        elif len(password) == 0:
            msg = "Please enter a password"
        elif password != rpassword:
            msg = "The password does not match"
        else:
            found = Users.query.filter_by(
                email=email,
            ).first()
            if found:
                msg = "The following email have already been registered"
            else:
                new_user = Users(first, last, email, password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("login"))
    return render_template("register.html", form=form, msg=msg)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
