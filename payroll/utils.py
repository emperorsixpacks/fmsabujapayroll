import logging
import os
import re
from datetime import datetime

import fitz  # PyMuPDF
from flask import flash

from payroll.config import Config
from payroll.models import Payslip, User, db

ALLOWED_EXTENSIONS = {"pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Configure logging
logging.basicConfig(
    filename="payslip_processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def sanitize_filename(filename):
    """Removes special characters and returns a clean filename."""
    filename = filename.lower()  # Convert to lowercase
    filename = os.path.splitext(filename)[0]  # Remove file extension
    filename = re.sub(
        r"[^a-zA-Z0-9]", "_", filename
    )  # Replace special characters with "_"
    return filename


def allowed_file(filename):
    """Check if file has a .pdf extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def file_size_ok(file):
    """Check if file size is within limit."""
    file.seek(0, os.SEEK_END)  # Move cursor to end of file
    size = file.tell()  # Get file size
    file.seek(0)  # Reset cursor for saving
    return size <= MAX_FILE_SIZE


def extract_payslips_from_pdf(pdf_path):
    """Extracts payslip pages and their IPPIS numbers from a PDF file."""
    logging.info(f"Extracting payslips from PDF: {pdf_path}")
    payslips = []  # Store (IPPIS, page_number) tuples

    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc):
            text = page.get_text("text")
            matches = re.findall(r"IPPIS\s*Number:\s*(\d+)", text)  # Extract the number

            if matches:
                ippis_number = matches[0]
                payslips.append((ippis_number, page_num))
                print(f"Found IPPIS {ippis_number} on page {page_num + 1}")

    if not payslips:
        logging.warning(f"No IPPIS numbers found in {pdf_path}")

    return payslips  # List of tuples: [(IPPIS1, page1), (IPPIS2, page2), ...]


def extract_payslip_page(pdf_path, output_path, payslip_page):
    """Extracts a single payslip page from the PDF and saves it as a new file."""
    logging.info(
        f"Extracting payslip page {payslip_page + 1} from {pdf_path} to {output_path}"
    )
    with fitz.open(pdf_path) as doc:
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=payslip_page, to_page=payslip_page)
        new_doc.save(output_path)
        new_doc.close()
    logging.info(f"Payslip page {payslip_page + 1} saved as {output_path}")


def process_payslip(temp_path, app):
    """Processes a payslip file, extracts IPPIS numbers for each page, and saves separately."""
    logging.info(f"Started processing payslip: {temp_path}")
    with app.app_context():  # Ensure database access inside the thread
        payslips = extract_payslips_from_pdf(temp_path)

        if not payslips:
            os.remove(temp_path)  # Clean up
            logging.warning(f"No valid payslips found in {temp_path}. File deleted.")
            return

        for ippis_number, payslip_page in payslips:
            # Find user by IPPIS number
            user = User.query.filter_by(ippis_number=ippis_number).first()
            if not user:
                logging.warning(
                    f"User with IPPIS {ippis_number} not found. Skipping page {payslip_page + 1}."
                )
                continue  # Skip to the next page if user not found

            # Generate filename with timestamp and page number
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            new_filename = f"{ippis_number}_{timestamp}.pdf"
            final_path = os.path.join(Config.UPLOAD_FOLDER, new_filename)

            # Extract and save the payslip page
            extract_payslip_page(temp_path, final_path, payslip_page)

            # Save to database
            new_payslip = Payslip(filename=new_filename, user_id=user.id)
            db.session.add(new_payslip)
            logging.info(f"Saved payslip for user {ippis_number}: {new_filename}")

        db.session.commit()
        os.remove(temp_path)  # Clean up original file
        logging.info(f"Completed processing for {temp_path}")
