import os

from flask import Blueprint, jsonify, render_template, request

from payroll.config import Config
from payroll.decorators import admin_required
from payroll.models import Payslip, db

payslipRouter = Blueprint("files", __name__)


@payslipRouter.route("/<int:payslip_id>/delete", methods=["POST"])
@admin_required
def delete_payslip(payslip_id):
    payslip = Payslip.query.get(payslip_id)

    if not payslip:
        return jsonify({"error": "Payslip not found"}), 404

    # Remove the actual file (optional)
    file_path = os.path.join(Config.UPLOAD_FOLDER, payslip.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete from DB
    db.session.delete(payslip)
    db.session.commit()

    return jsonify({"message": "Payslip deleted successfully"}), 200


@payslipRouter.route("/", methods=["GET"])
@admin_required
def list_payslips():
    page = request.args.get(
        "page", 1, type=int
    )  # Get current page number, default to 1
    per_page = 10  # Define how many payslips to display per page
    payslips = Payslip.query.paginate(
        page, per_page, False
    )  # Paginate the payslips query

    return render_template("admin/payslips.html", payslips=payslips)
