from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, FileUploadForm
from app.models import User
from app.cloud_utils import process_file


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    The route for the registration page of the application.

    Returns:
    --------
    str
        The rendered template for the registration page.
    """
    if current_user.is_authenticated and request.method == "GET":
        flash("You are already logged in. Please log out first.", "warning")
        return redirect(url_for("upload"))
    if request.method == "POST":
        form = RegistrationForm()
        if form.validate_on_submit():
            full_name = form.full_name.data
            email = form.email.data
            # check if email already exists
            user = User.query.filter_by(email=email).first()
            if user:
                flash("Email already exists", "warning")
                return redirect(url_for("register"))
            password = form.password.data
            confirm_password = form.confirm_password.data
            # check if passwords match
            if password != confirm_password:
                flash("Passwords do not match", "warning")
                return redirect(url_for("register"))
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            user = User(full_name=full_name, email=email, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("You have been registered successfully!", "success")
            return redirect(url_for("login"))
        # if user is already logged in, flash message to log out first and redirect to upload page
    else:
        form = RegistrationForm()

    return render_template(
        "register.html", title="Register", form=form, active_page="register"
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    The route for the login page of the application.

    Returns:
    --------
    str
        The rendered template for the login page.
    """

    if request.method == "POST":
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                flash("Invalid email. Try Again", "warning")
                return redirect(url_for("login"))
            if not user.check_password(form.password.data):
                flash("Invalid password. Try Again", "warning")
                return redirect(url_for("login"))
            flash("You have been logged in!", "success")
            login_user(user)
            return redirect(url_for("upload"))
    else:
        form = LoginForm()
    return render_template("index.html", title="Login", form=form, active_page="login")


@app.route("/")
def index():
    """
    The route for the index page of the application.
    If the user is authenticated, redirect to the upload page. If not redirect to the login page.

    Returns:
    --------
    str
        The rendered template for the index page.
    """
    if current_user.is_authenticated:
        return redirect(url_for("upload"))
    else:
        return redirect(url_for("login"))


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        form = FileUploadForm()
        if form.validate_on_submit():
            file = form.file.data
            emails = form.emails.data
            process_file(file, emails)
            flash("File uploaded successfully!", "success")
            return redirect(url_for("upload"))
        else:
            flash("File Upload Failed. Try Again", "warning")
    else:
        form = FileUploadForm()
    return render_template(
        "upload.html", title="Upload", active_page="upload", form=form
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", "success")
    return redirect(url_for("login"))
