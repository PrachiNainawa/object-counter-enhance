from io import BytesIO
import json
import os
import pytest
from flask import Flask
from flask.testing import FlaskClient

# Import your app and other necessary functions from the main code
from counter.entrypoints.webapp import app

@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_base_route(client: FlaskClient):
    """Test the base route."""
    response = client.get('/')
    assert response.status_code == 200

def test_object_count_route(client: FlaskClient):
    """Test the object_count route."""
    data = {'threshold': 0.5}
    image_path = 'resources/images/blank.jfif'  # Adjust the path accordingly
    with open(image_path, 'rb') as image_file:
        data['file'] = (image_file, 'image.jpg')
        response = client.post('/object-count', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        response_data = json.loads(response.get_data(as_text=True))
        assert 'current_objects' in response_data and 'total_objects' in response_data
        assert 'count' in response_data['current_objects'][0] if len(response_data['current_objects'])>0 else 'count'

def test_predict_objects_by_img_route(client: FlaskClient):
    """Test the predict_objects_by_img route."""
    data = {'threshold': 0.5}
    image_path = 'resources/images/blank.jfif'  # Adjust the path accordingly
    with open(image_path, 'rb') as image_file:
        data['file'] = (image_file, 'image.jpg')
        response = client.post('/predict-objects-by-img', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        response_data = json.loads(response.get_data(as_text=True))
        assert 'current_objects' in response_data and 'total_objects' in response_data
        # breakpoint()
        assert 'count' in response_data['current_objects'][0] if len(response_data['current_objects'])>0 else 'count'
