from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func, or_

from payroll.decorators import admin_required
from payroll.models import Payslip, User, db

userRouter = Blueprint("users", __name__)


@userRouter.route("/profile", methods=["GET", "POST"])
@login_required  # Ensure only logged-in users can access
def profile():
    user = current_user  # Get logged-in user

    if request.method == "POST":
        user.first_name = request.form.get("first_name")
        user.last_name = request.form.get("last_name")
        user.email = request.form.get("email")

        db.session.commit()
        flash("Profile updated successfully", "success")
        return redirect(url_for("users.profile"))  # Reload profile page

    return render_template("profile.html", user=user)

@userRouter.route("/", methods=["GET"])
@login_required  # Assuming admin_required is similar to login_required
def list_users():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    search_query = request.args.get("search", "").strip()
    base_query = User.query

    if search_query:
        search_term = f"%{search_query}%"
        base_query = base_query.filter(
            or_(
                User.email.ilike(search_term),
                User.first_name.ilike(search_term),
                User.last_name.ilike(search_term),
                func.concat(User.first_name, " ", User.last_name).ilike(
                    search_term
                ),  # Fix for full name search
            )
        )

    # Apply ordering and paginate
    users_paginated = base_query.order_by(User.last_name, User.first_name).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # HTMX request handling
    if request.headers.get("HX-Request"):
        return render_template("partials/user_list.html", users=users_paginated)

    return render_template("admin/users.html", users=users_paginated)


@userRouter.route("/<int:user_id>/delete", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        flash("User not found", "error")
        return redirect(url_for("list_users"))

    # Admin deleting a user, perform deletion
    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully", "success")
    return "", 200

@userRouter.route("/payslips", methods=["GET"])
@login_required
def get_user_payslips():
    page = request.args.get("page", 1, type=int)
    payslips = Payslip.query.filter_by(user_id=current_user.id).paginate(
        page, 10, False
    )

    return render_template("user_payslips.html", payslips=payslips)


@userRouter.route("/search")
def search_users():
    search = request.args.get("search", "").strip()

    query = User.query
    if search:
        query = query.filter(
            or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
            )
        )

    users = query.limit(10).all()

    return render_template("partials/users_options.html", users=users)
    
