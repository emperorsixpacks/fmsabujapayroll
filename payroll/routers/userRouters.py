from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from payroll.decorators import admin_required
from payroll.models import Payslip, User, db

userRouter = Blueprint("users", __name__)


@userRouter.route("")
@admin_required
def get_all_users():
    users = User.query.all()
    return render_template("admin/users.html", users=users)


@userRouter.route("/<int:user_id>")
@admin_required
def get_user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    payslips = Payslip.query.filter_by(user_id=user.id).all()
    return render_template("admin/user_detail.html", user=user, payslips=payslips)


@userRouter.route("/<int:user_id>/delete", methods=["POST"])
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
    return redirect(url_for("list_users"))


@userRouter.route("/update", methods=["POST"])
@login_required
def update_user():
    # Get user data from the form
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    # Ensure required fields are present
    if not name and not email:
        flash("At least one field (name or email) is required", "error")
        return redirect(url_for("user_profile"))

    # Update the current user details
    if name:
        current_user.name = name
    if email:
        current_user.email = email

    db.session.commit()

    flash("User data updated successfully!", "success")
    return redirect(url_for("user_profile"))


@userRouter.route("/payslips", methods=["GET"])
@login_required
def get_user_payslips():
    page = request.args.get("page", 1, type=int)
    payslips = Payslip.query.filter_by(user_id=current_user.id).paginate(
        page, 10, False
    )

    return render_template("user_payslips.html", payslips=payslips)


@userRouter.route("/dashboard")
@login_required
def dashboard():
    payslips = Payslip.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", payslips=payslips)
