from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_required

from payroll.config import Config
from payroll.models import User, db
from payroll.routers import authRouter, fileRouter, payslipRouter, userRouter

app = Flask("__name__")
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user/config")
@login_required
def user_config():
    return render_template("user_config.html", user=current_user)


app.register_blueprint(authRouter, url_prefix="/auth")
app.register_blueprint(fileRouter, url_prefix="/files")
app.register_blueprint(userRouter, url_prefix="/users")
app.register_blueprint(payslipRouter, url_prefix="/slip")


def run():
    with app.app_context():
        db.create_all()  # Ensure the database is created
    app.run(debug=True)
