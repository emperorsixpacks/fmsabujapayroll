import os

from flask import Blueprint, jsonify, render_template

from payroll.config import Config
from payroll.decorators import admin_required
from payroll.models import Payslip, db

payslipRouter = Blueprint("files", __name__)


@payslipRouter.route("/payslips/<int:payslip_id>/delete", methods=["POST"])
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


@payslipRouter.route("/payslips", methods=["GET"])
@admin_required
def list_payslips():
    payslips = Payslip.query.all()
    return render_template("admin/payslips.html", payslips=payslips)
