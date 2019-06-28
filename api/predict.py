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

from core.model import ModelWrapper

from maxfw.core import MAX_API, PredictAPI

from flask_restplus import Namespace, Resource, fields
from flask import request
from config import MODEL_META_DATA, DEFAULT_CHARS


model_input = MAX_API.model('ModelInput', {
    'seed_text': fields.String(required=True, description='Text to seed generative model'),
    'chars': fields.Integer(default=DEFAULT_CHARS, required=False, description='Number of characters to generate')
})

model_prediction = MAX_API.model('ModelPrediction', {
    'seed_text': fields.String(required=True, description='Seed text used to generate new text'),
    'generated_text': fields.String(required=True, description='Text generated by the model'),
    'full_text': fields.String(required=False, description='Seed text followed by generated text')
})


class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc('predict')
    @MAX_API.expect(model_input)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        j = request.get_json()
        seed_text = j['seed_text']
        gen_chars = j['chars'] if 'chars' in j else DEFAULT_CHARS
        generated_text = self.model_wrapper._predict(seed_text, gen_chars)
        full_text = seed_text + generated_text
        model_pred = {
            'seed_text': seed_text,
            'generated_text': generated_text,
            'full_text': full_text
        }
        result['prediction'] = model_pred
        result['status'] = 'ok'

        return result
