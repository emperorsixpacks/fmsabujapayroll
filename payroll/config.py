import os


def return_base_dir(current_location):
    """
    Params:
    current_dir: the current file name or path
    Returns the base dir, relative to the current working dir
    """
    return os.path.dirname(os.path.dirname(current_location))


BASE_DIR = return_base_dir(__file__)


class Config:
    SECRET_KEY = "QY7TdA5r+vj6kHbNALGgbcER4vvOyI4CgOVCseicAjg="
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, "pages")
    STATIC_FOLDER = os.path.join(BASE_DIR, "static")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
