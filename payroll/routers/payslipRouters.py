import logging
import os
import threading
from datetime import datetime

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy import extract, or_

from payroll.config import Config
from payroll.decorators import admin_required
from payroll.models import Payslip, User, db
from payroll.utils import allowed_file, file_size_ok, process_payslip, sanitize_filename

payslipRouter = Blueprint("slips", __name__)

# Configure logging to log both to a file and the console
logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("payslip_processing.log"),  # Log to a file
        logging.StreamHandler(),  # Log to the console
    ],
)


@payslipRouter.route("/<int:payslip_id>/delete", methods=["DELETE"])
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

    return "", 200


@payslipRouter.route("/", methods=["GET"])
@admin_required  # Assuming admin_required is similar to login_required
def list_payslips():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    search_query = request.args.get("search", "").strip()
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    # Base query with join to access user details
    base_query = Payslip.query.join(User)

    # Apply filters if provided
    if search_query:
        search_term = f"%{search_query}%"
        base_query = base_query.filter(
            or_(
                User.first_name.ilike(search_term),
                User.last_name.ilike(search_term),
                Payslip.filename.ilike(search_term),
            )
        )

    if year:
        base_query = base_query.filter(extract("year", Payslip.upload_date) == year)

    if month:
        base_query = base_query.filter(extract("month", Payslip.upload_date) == month)

    # Apply ordering and paginate
    payslips_paginated = base_query.order_by(Payslip.upload_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template(
        "admin/payslips.html", payslips=payslips_paginated, datetime=datetime
    )


@payslipRouter.route("/my-payslips", methods=["GET"])
@login_required
def my_payslips():
    page = request.args.get("page", 1, type=int)
    per_page = 10  # Get month and year from query parameters
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)

    # Start with all payslips belonging to the current logged-in user
    query = Payslip.query.filter_by(user_id=current_user.id)

    # Apply filtering if month and year are provided
    if month and year:
        query = query.filter(
            db.extract("year", Payslip.upload_date) == year,
            db.extract("month", Payslip.upload_date) == month,
        )

    # Order by upload date (most recent first)
    payslips = query.order_by(Payslip.upload_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template("user_payslips.html", payslips=payslips, datetime=datetime)


@payslipRouter.route("/my-payslip-search", methods=["GET"])
@login_required
def my_payslip_search():
    """Limit search to only the current user's payslips."""
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    # Base query limited to current user
    base_query = Payslip.query.filter(Payslip.user_id == current_user.id)

    if year:
        base_query = base_query.filter(extract("year", Payslip.upload_date) == year)

    if month:
        base_query = base_query.filter(extract("month", Payslip.upload_date) == month)

    payslips = base_query.order_by(Payslip.upload_date.desc()).all()

    return render_template("partials/user_payslips_list.html", payslips=payslips)


@payslipRouter.route("/search", methods=["GET"])
@admin_required
def search_payslips():
    search_query = request.args.get("search", "").strip()
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    # Base query
    base_query = Payslip.query.join(User)

    # Apply filters
    if search_query:
        search_term = f"%{search_query}%"
        base_query = base_query.filter(
            or_(
                User.first_name.ilike(search_term),
                User.last_name.ilike(search_term),
                Payslip.filename.ilike(search_term),
            )
        )

    if year:
        base_query = base_query.filter(extract("year", Payslip.upload_date) == year)

    if month:
        base_query = base_query.filter(extract("month", Payslip.upload_date) == month)

    payslips = base_query.order_by(Payslip.upload_date.desc()).all()

    return render_template("partials/payslip_list.html", payslips=payslips)


@payslipRouter.route("/create", methods=["GET", "POST"])
@admin_required
def create_payslip():
    if request.method == "POST":
        payslip_file = request.files.get("payslip")

        if not payslip_file or payslip_file.filename == "":
            flash("Please upload a payslip file.", "danger")
            return redirect(url_for("slips.create_payslip"))

        if not allowed_file(payslip_file.filename):
            flash("Only PDF files are allowed.", "danger")
            return redirect(url_for("slips.create_payslip"))

        if not file_size_ok(payslip_file):
            flash("File size must be less than 1MB.", "danger")
            return redirect(url_for("slips.create_payslip"))

        # Extract IPPIS number from filename (assuming format like "123456.pdf")
        ippis_number = os.path.splitext(payslip_file.filename)[0]

        # Find user by IPPIS number
        user = User.query.filter_by(ippis_number=ippis_number).first()
        if not user:
            flash(f"User with IPPIS number {ippis_number} not found.", "danger")
            return redirect(url_for("slips.create_payslip"))

        # Rename file with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        new_filename = f"{ippis_number}_{timestamp}.pdf"
        file_path = os.path.join(Config.UPLOAD_FOLDER, new_filename)
        payslip_file.save(file_path)

        # Save to database
        new_payslip = Payslip(filename=new_filename, user_id=user.id)
        db.session.add(new_payslip)
        db.session.commit()

        flash("Payslip uploaded successfully!", "success")
        return redirect(url_for("slips.list_payslips"))

    return render_template("admin/create_payslip.html")


@payslipRouter.route("/bulk-upload", methods=["GET", "POST"])
@admin_required
def bulk_upload_payslips():
    if request.method == "POST":
        payslip_files = request.files.getlist("payslips")  # Get multiple files

        if not payslip_files or all(f.filename == "" for f in payslip_files):
            flash("Please upload at least one payslip file.", "danger")
            return redirect(url_for("slips.bulk_upload_payslips"))

        # Save files before starting threads
        saved_files = []
        for payslip_file in payslip_files:
            if not allowed_file(payslip_file.filename):
                flash(f"Invalid file type: {payslip_file.filename}", "danger")
                logging.warning(f"Invalid file type uploaded: {payslip_file.filename}")
                continue  # Skip invalid files

            if not file_size_ok(payslip_file):
                flash(f"File too large: {payslip_file.filename}", "danger")
                logging.warning(f"File too large: {payslip_file.filename}")
                continue  # Skip large files

            # Generate a clean filename with timestamp
            clean_name = sanitize_filename(payslip_file.filename)
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            temp_filename = f"{clean_name}_{timestamp}.pdf"
            temp_path = os.path.join(Config.UPLOAD_FOLDER, temp_filename)

            # Save file to disk
            payslip_file.save(temp_path)
            saved_files.append(temp_path)
            logging.info(f"File saved: {temp_path}")

        # Start processing in separate threads
        for temp_path in saved_files:
            thread = threading.Thread(
                target=process_payslip,
                args=(temp_path, current_app._get_current_object()),
            )
            thread.start()
            logging.info(f"Started thread for {temp_path}")

        flash("Payslips are being processed in the background!", "success")
        return redirect(url_for("slips.list_payslips"))

    return render_template("admin/bulk_upload_payslips.html")
