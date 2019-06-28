#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import pytest
import requests


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'MAX Review Text Generator'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'generative-language-model-keras'
    assert metadata['name'] == 'Generative Language Model Keras'
    assert metadata['description'] == 'Generative Language Model in Keras trained on Yelp reviews'
    assert metadata['license'] == 'Apache2'
    assert metadata['type'] == 'Language Modeling'
    assert 'max-review-text-generator' in metadata['source']


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
