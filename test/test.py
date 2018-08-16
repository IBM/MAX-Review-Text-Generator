import pytest
import pycurl
import io
import json


def test_response():
    seed_text = "went there for dinner on a friday night and i have to say i'm impressed by the quality of the food "
    chars = 20

    c = pycurl.Curl()
    b = io.BytesIO()
    c.setopt(pycurl.URL, 'http://localhost:5000/model/predict')
    c.setopt(pycurl.HTTPHEADER, ['Accept:application/json', 'Content-Type: application/json'])

    c.setopt(pycurl.POSTFIELDS, '{"seed_text": "' + seed_text + '", "chars": ' + str(chars) + '}')
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.perform()
    assert c.getinfo(pycurl.RESPONSE_CODE) == 200
    c.close()

    response = b.getvalue()
    response = json.loads(response)

    assert response['status'] == 'ok'
    assert response['prediction']['seed_text'] == seed_text
    assert len(response['prediction']['generated_text']) == chars

    assert response['prediction']['full_text'] == seed_text + response['prediction']['generated_text']


if __name__ == '__main__':
    pytest.main([__file__])
