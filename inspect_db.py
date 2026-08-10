import os
from app import create_app
from app.models.rbac import User

app = create_app()
with app.app_context():
    print('URI', app.config['SQLALCHEMY_DATABASE_URI'])
    print('DB exists?', os.path.exists('app.db'))
    print('User count', User.query.count())
    for user in User.query.all():
        print(user.id, user.email, user.role_id)
