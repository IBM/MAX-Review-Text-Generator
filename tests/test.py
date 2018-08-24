import pytest
import requests


def test_response():
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
