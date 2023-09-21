from io import BytesIO
import json
import os
import pytest
from flask.testing import FlaskClient
from dotenv import load_dotenv
load_dotenv()

# Import your app and other necessary functions from the main code
from counter.entrypoints.webapp import app

@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

@pytest.fixture()
def resource_path():
    return 'resources/images/'

@pytest.fixture()
def get_img(resource_path):
    """Returns the image mentioned"""
    image_path = resource_path

    def _specify_name(img_name):
        with open(image_path+img_name, 'rb') as image_file:
            data = BytesIO(image_file.read())
            img_data = (data, img_name)
        return img_data
        
    yield _specify_name


def test_base_route(client: FlaskClient):
    """Test the base route."""
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.parametrize("img_name,route,db,threshold", [
    ('boy.jpg', '/object-count', 'mongo',1),
    ('blank.jfif', '/object-count', 'postgres',0.5),
    ('cat.jpg', '/predict-objects-by-img', 'postgres',0.3),
    ])
def test_object_count_routes(client: FlaskClient,get_img, img_name, route, db, threshold):
    """Test the object_count routes based on different parameters"""
    os.environ['DB']=db
    data = {'threshold': threshold}
    data['file'] = get_img(img_name=img_name)
    response = client.post(route, data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    response_data = json.loads(response.get_data(as_text=True))
    assert 'current_objects' in response_data and 'total_objects' in response_data
    assert 'count' in response_data['current_objects'][0] if len(response_data['current_objects'])>0 else 'count'
