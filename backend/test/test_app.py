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

@pytest.fixture
def create_sample_diary():
    response = client.post('/diaries', json={'title': 'Test Title', 'content': 'Test Content'})
    return response.json['id']

def test_get_diary(client):
    response = client.put(f'/diaries/1', json={'title': 'Updated Title', 'content': 'Updated Content'})
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Title'
    assert response.json['content'] == 'Updated Content'

# url path로 넘겨받은 id가 db에 존재하지 않을 때
def test_update_diary_not_found(client):
    response = client.put('/diaries/99999', json={'title': 'Updated Title', 'content': 'Updated Content'})
    assert response.status_code == 404
    assert response.json['error'] == 'Diary Not Found'

def test_다이어리_삭제_성공시(client):
    response = client.delete(f'/diaries/1')
    assert response.status_code == 200

def test_없는_다이어리_삭제_시도(client):
    response = client.delete(f'/diaries/99999')
    assert response.status_code == 404
    assert response.json['error'] == 'Diary Not Found'