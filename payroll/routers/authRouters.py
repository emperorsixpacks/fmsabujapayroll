from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from payroll.models import User, db
from payroll.decorators import admin_required

authRouter = Blueprint("auth", __name__)


@authRouter.route("/register", methods=["GET", "POST"])
@admin_required
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        last_name = request.form["lastName"]
        first_name = request.form["firstName"]
        ippis_number = request.form["ippisNumber"]  # Get IPPIS number from form

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is already registered. Please log in.", "danger")
            return redirect(url_for("auth.register"))

        # Check if the IPPIS number already exists
        existing_ippis = User.query.filter_by(ippis_number=ippis_number).first()
        if existing_ippis:
            flash("IPPIS Number is already in use. Please check and try again.", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)
        user = User(
            email=email,
            password_hash=hashed_password,
            role="employee",
            first_name=first_name,
            last_name=last_name,
            ippis_number=ippis_number,  # Save IPPIS number
        )
        db.session.add(user)
        db.session.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for("users.list_users"))

    return render_template("admin/create_user.html")

@authRouter.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # Redirect the user to a different page if they're already logged in
        return redirect(url_for("slips.my_payslips"))
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found. Please register.", "danger")
        elif not check_password_hash(user.password_hash, password):
            flash("Incorrect password. Please try again.", "danger")
        else:
            login_user(user)
            return redirect(url_for("slips.my_payslips"))

    return render_template("login.html")


@authRouter.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
