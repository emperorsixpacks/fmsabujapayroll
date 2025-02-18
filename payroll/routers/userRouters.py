from flask import Blueprint, render_template
from flask_login import current_user, login_required

from payroll.decorators import admin_required
from payroll.models import Payslip, User

userRouter = Blueprint("users", __name__)


@userRouter.route("/users")
@admin_required
def get_all_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@userRouter.route("/users/<int:user_id>")
@admin_required
def get_user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    payslips = Payslip.query.filter_by(user_id=user.id).all()
    return render_template("user_detail.html", user=user, payslips=payslips)


@userRouter.route("/dashboard")
@login_required
def dashboard():
    payslips = Payslip.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", payslips=payslips)
