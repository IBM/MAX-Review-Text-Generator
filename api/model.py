from flask_restplus import Namespace, Resource, fields
from flask import request
from config import MODEL_META_DATA, DEFAULT_CHARS
from core.backend import ModelWrapper

api = Namespace('model', description='Model information and inference operations')

model_meta = api.model('ModelMetadata', {
    'id': fields.String(required=True, description='Model identifier'),
    'name': fields.String(required=True, description='Model name'),
    'description': fields.String(required=True, description='Model description'),
    'license': fields.String(required=False, description='Model license')
})


@api.route('/metadata')
class Model(Resource):
    @api.doc('get_metadata')
    @api.marshal_with(model_meta)
    def get(self):
        """Return the metadata associated with the model"""
        return MODEL_META_DATA


model_input = api.model('ModelInput', {
    'seed_text': fields.String(required=True, description='Text to seed generative model'),
    'chars': fields.Integer(default=DEFAULT_CHARS, required=False, description='Number of characters to generate')
})

model_prediction = api.model('ModelPrediction', {
    'seed_text': fields.String(required=True, description='Seed text used to generate new text'),
    'generated_text': fields.String(required=True, description='Text generated by the model'),
    'full_text': fields.String(required=False, description='Seed text followed by generated text')
})


@api.route('/predict')
class Predict(Resource):

    model_wrapper = ModelWrapper()

    @api.doc('predict')
    @api.expect(model_input)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        j = request.get_json()
        seed_text = j['seed_text']
        gen_chars = j['chars'] if 'chars' in j else DEFAULT_CHARS
        generated_text = self.model_wrapper.predict(seed_text, gen_chars)
        full_text = seed_text + generated_text
        model_pred = {
            'seed_text': seed_text,
            'generated_text': generated_text,
            'full_text': full_text
        }
        result['prediction'] = model_pred
        result['status'] = 'ok'

        return result
