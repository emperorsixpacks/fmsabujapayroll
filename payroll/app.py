from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate

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
    return redirect(url_for("slips.my_payslips"))

app.register_blueprint(authRouter, url_prefix="/auth")
app.register_blueprint(fileRouter, url_prefix="/files")
app.register_blueprint(userRouter, url_prefix="/users")
app.register_blueprint(payslipRouter, url_prefix="/slip")

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)