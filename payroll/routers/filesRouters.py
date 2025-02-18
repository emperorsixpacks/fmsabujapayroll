import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from payroll.config import Config
from payroll.models import Payslip, User, db

fileRouter = Blueprint("files", __name__)


@fileRouter.route("/admin/upload", methods=["GET", "POST"])
@login_required
def upload_payslip():
    if not current_user.is_admin():
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        file = request.fileRouter["payslip"]
        user_id = request.form["user_id"]  # Employee ID

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)

            payslip = Payslip(filename=filename, user_id=user_id)
            db.session.add(payslip)
            db.session.commit()

            flash("Payslip uploaded successfully.", "success")

    employees = User.query.filter_by(role="employee").all()
    return render_template("admin_upload.html", employees=employees)
