from payroll.routers.authRouters import authRouter
from payroll.routers.filesRouters import fileRouter
from payroll.routers.payslipRouters import payslipRouter
from payroll.routers.userRouters import userRouter

__all__ = ["authRouter", "fileRouter", "userRouter", "payslipRouter"]
