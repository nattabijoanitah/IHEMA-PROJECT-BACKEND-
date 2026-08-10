from app import create_app
from app.extensions import db
from app.models.rbac import User, Role

app = create_app()
app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')

with app.app_context():
    db.drop_all()
    db.create_all()
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()
    user = User(full_name='Admin', email='admin@example.com', role=role)
    user.set_password('secret')
    db.session.add(user)
    db.session.commit()
    client = app.test_client()
    login = client.post('/api/auth/login', json={'email': 'admin@example.com', 'password': 'secret'})
    print('login_status', login.status_code)
    token = login.get_json()['access_token']
    resp = client.get('/api/admin/dashboard', headers={'Authorization': f'Bearer {token}'})
    print('dashboard_status', resp.status_code)
    print(resp.get_json())
