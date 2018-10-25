import pytest
import requests


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'Model Asset Exchange Server'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'generative-language-model-keras'
    assert metadata['name'] == 'Generative Language Model Keras'
    assert metadata['description'] == 'Generative Language Model in Keras trained on Yelp reviews'
    assert metadata['license'] == 'Apache2'


def test_predict():
    seed_text = "went there for dinner on a friday night and i have to say i'm impressed by the quality of the food "
    chars = 20
    model_endpoint = 'http://localhost:5000/model/predict'

    json_data = {"seed_text": seed_text, "chars": chars}

    r = requests.post(url=model_endpoint, json=json_data)

    assert r.status_code == 200

    response = r.json()

    assert response['status'] == 'ok'
    assert response['prediction']['seed_text'] == seed_text
    assert len(response['prediction']['generated_text']) == chars

    assert response['prediction']['full_text'] == seed_text + response['prediction']['generated_text']


if __name__ == '__main__':
    pytest.main([__file__])
