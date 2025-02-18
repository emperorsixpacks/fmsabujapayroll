import os

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

from payroll.config import Config
from payroll.decorators import admin_required
from payroll.models import Payslip, User, db

fileRouter = Blueprint("files", __name__)
ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@fileRouter.route("/upload", methods=["POST"])
@admin_required
def upload_payslip():
    if "file" not in request.files:
        flash("No file part", "error")
        return redirect(request.referrer)

    file = request.files["file"]
    user_id = request.form.get("user_id")

    # If no file is selected
    if file.filename == "":
        flash("No selected file", "error")
        return redirect(request.referrer)

    # Ensure the file is allowed
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        user = User.query.get(user_id)
        if not user:
            flash("User not found", "error")
            return redirect(request.referrer)

        # Save file to the uploads folder
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))

        # Save filename (not full path) in the database
        payslip = Payslip(filename=filename, user_id=user_id)
        db.session.add(payslip)
        db.session.commit()

        flash("Payslip uploaded successfully!", "success")
        return redirect(url_for("list_payslips"))  # Redirect to payslip listing
    else:
        flash("Invalid file type! Only PDFs are allowed.", "error")
        return redirect(request.referrer)


@fileRouter.route("/download/<int:payslip_id>", methods=["GET"])
@admin_required
def download_payslip(payslip_id):
    payslip = Payslip.query.get(payslip_id)

    if not payslip:
        abort(404, description="Payslip not found")

    return send_from_directory(
        Config.UPLOAD_FOLDER, payslip.filename, as_attachment=True
    )
