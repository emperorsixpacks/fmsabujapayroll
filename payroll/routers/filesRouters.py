import os

from config import Config
from flask import Blueprint, flash, redirect, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

files = Blueprint("files", __name__)


@files.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file uploaded")
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
    flash("File uploaded successfully")
    return redirect(url_for("home.index"))


@files.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)
