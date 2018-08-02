# Application settings

# Flask settings 
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# API metadata
API_TITLE = 'Model Asset Exchange Server'
API_DESC = 'An API for serving models'
API_VERSION = '0.1'

# default model
MODEL_NAME = 'Generative Language Model'
DEFAULT_MODEL_PATH = 'assets'
DEFAULT_MODEL_FILE = 'generative_lang_model.h5'
DEFAULT_CHARS = 100
# for image models, may not be required
MODEL_INPUT_IMG_SIZE = None
MODEL_LICENSE = 'Apache2'

# (Fixed) length of seed text that can serve as input to the generative model.
# Must match the compiled model referenced by DEFAULT_MODEL_FILE
SEED_TEXT_LEN = 256


MODEL_META_DATA = {
    'id': '{}-keras'.format(MODEL_NAME.lower().replace(' ', '-')),
    'name': '{} Keras'.format(MODEL_NAME),
    'description': '{} in Keras trained on Yelp reviews'.format(MODEL_NAME),
    'type': 'language_modeling',
    'license': '{}'.format(MODEL_LICENSE)
}
