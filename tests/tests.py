import pytest
from app import create_app, db
from app.models import User, Owner
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

@pytest.fixture
def app():
    app = create_app(testing=True) 
    with app.app_context():
        db.create_all() 
        yield app
        db.drop_all()  
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    user = User(name='testuser', password='testpassword')  
    hashed_password = bcrypt.generate_password_hash(user.password).decode('utf-8')
    user.password = hashed_password

    db.session.add(user)
    db.session.commit()

    owner = Owner(name='Marcos testes')
    db.session.add(owner)
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()

def test_login(client, init_db):
    response = client.post('/v1/login', json={'username': 'testuser', 'password': 'testpassword'})
    data = response.get_json()
    assert response.status_code == 200
    assert 'access_token' in data

def test_add_owner(client, init_db):
    login_response = client.post('/v1/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = login_response.get_json()['access_token']

    response = client.post('/v1/owners', json={'name': 'Marcos Testes'}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert response.get_json()['message'] == "Owner added successfully."

def test_add_car(client, init_db):
    login_response = client.post('/v1/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = login_response.get_json()['access_token']

    response = client.post('/v1/owners/1/cars', json={'color': 'blue', 'model': 'sedan'}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert response.get_json()['message'] == "Car added successfully."

def test_get_owners(client, init_db):
    login_response = client.post('/v1/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = login_response.get_json()['access_token']

    response = client.get('/v1/owners', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert len(response.get_json()) > 0

def test_get_owner(client, init_db):
    login_response = client.post('/v1/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = login_response.get_json()['access_token']

    response = client.get('/v1/owners/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'Marcos testes' in response.get_json()['name']

def test_get_car(client, init_db):
    login_response = client.post('/v1/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = login_response.get_json()['access_token']

    client.post('/v1/owners/1/cars', json={'color': 'blue', 'model': 'sedan'}, headers={'Authorization': f'Bearer {token}'})
    response = client.get('/v1/cars/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'blue' in response.get_json()['color']
