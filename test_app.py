import pytest
from flask import url_for
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/index')
    assert response.status_code == 200

def test_user_register_route(client):
    response = client.post('/userregister', data={'username': 'test_user', 'password': 'test_password'})
    assert response.status_code == 200  # Redirects to login route upon successful registration

def test_login_route(client):
    response = client.post('/login', data={'username': 'test_user', 'password': 'test_password'}, follow_redirects=True)
    assert response.status_code == 200  # Successful login redirects to estimation route
    #assert b'Estimation List' in response.data  # Checking if estimation list is present in response

def test_estimation_route(client):
    response = client.get('/estimation')
    assert response.status_code == 200

def test_estimation_data_route(client):
    response = client.get('/estimation_data')
    assert response.status_code == 200

# def test_update_estimation_route(client):
#     # Assuming an existing estimation ID
#     response = client.post('/update/your_estimation_id', data={'taskName': 'Updated Task'})
#     assert response.status_code == 302  # Redirects to estimation list route after updating

# def test_delete_estimation_route(client):
#     # Assuming an existing estimation ID
#     response = client.get('/delete/your_estimation_id')
#     assert response.status_code == 302  # Redirects to estimation list route after deleting

# def test_logout_route(client):
#     response = client.get('/logout')
#     assert response.status_code == 302  # Redirects to login route after logout
