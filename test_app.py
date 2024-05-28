import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/index')
    assert response.status_code == 200
    

def test_user_register(client):
    response = client.post('/userregister', data={'username': 'ram401', 'password': 'Ram401'})
    assert response.status_code == 200  # Redirects after successful registration

def test_login(client):
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 302  # Redirects after successful login

def test_estimation(client):
    response = client.post('/estimation', data={'taskName': 'Test Task', 'complexity': 'low', 'size': 'small', 'taskType': 'type'})
    assert response.status_code == 200
    assert b'Estimated Effort' in response.data

def test_show_estimations(client):
    response = client.get('/estimation_data')
    assert response.status_code == 200
    # Add more assertions based on your estimation list template

def test_update_form(client):
    # Assuming you have some data in your estimation collection for testing
    test_id = 'some_id'
    response = client.post(f'/update_form/{test_id}', data={'task_title': 'Updated Task'})
    assert response.status_code == 500 # Redirects after successful update

def test_delete_estimation(client):
    # Assuming you have some data in your estimation collection for testing
    test_id = 'some_id'
    response = client.get(f'/delete/{test_id}')
    assert response.status_code == 500  # Redirects after successful deletion

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302  # Redirects after logout
