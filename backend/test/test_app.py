import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_diaries(client):
    response = client.get('/diaries')
    assert response.status_code == 200
    assert response.json == []

def test_create_diary(client):
    response = client.post('/diaries', json={'title': 'Test Title', 'content': 'Test Content'})
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['title'] == 'Test Title'
    assert response.json['content'] == 'Test Content'

def test_create_diary_missing_title(client):
    response = client.post('/diaries', json={'content': 'Test Content'})
    assert response.status_code == 400
    assert response.json == {'error': 'Title and Content are required'}

def test_create_diary_missing_content(client):
    response = client.post('/diaries', json={'title': 'Test Title'})
    assert response.status_code == 400
    assert response.json == {'error': 'Title and Content are required'}