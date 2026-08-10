from app import create_app
from app.models.rbac import User

app = create_app()

with app.app_context():
    user = User()
    user.set_password('password')
    print('generated_hash', user.password_hash)
    print('check_password', user.check_password('password'))
    print('check_wrong_password', user.check_password('wrong'))
