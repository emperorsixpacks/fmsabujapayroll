from flask import Blueprint, render_template
from flask_login import current_user, login_required

from payroll.models import Payslip

userRouter = Blueprint("users", __name__)


@userRouter.route("/dashboard")
@login_required
def dashboard():
    payslips = Payslip.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", payslips=payslips)
