from keras.backend import clear_session
from keras import models
import tensorflow as tf
import numpy as np
import json
import logging

logger = logging.getLogger()

from config import DEFAULT_MODEL_PATH, DEFAULT_MODEL_FILE, SEED_TEXT_LEN

# (Fixed) length of seed text that can serve as input to the generative model
_SEED_TEXT_LEN = 256

class ModelWrapper(object):


    """Model wrapper for Keras models"""
    def __init__(self, path=DEFAULT_MODEL_PATH, model_file=DEFAULT_MODEL_FILE):
        logger.info('Loading model from: {}...'.format(path))
        model_path = '{}/{}'.format(path, model_file)
        clear_session()
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.model = models.load_model(model_path)
            logger.info('Loaded model: {}'.format(self.model.name))
        self._load_assets(path)

    def _load_assets(self, path):
        with open('{}/char_indices.txt'.format(path)) as f:
            self.char_indices = json.loads(f.read())
            self.chars = sorted(self.char_indices.keys())
            self.num_chars = len(self.chars)
        with open('{}/indices_char.txt'.format(path)) as f:
            self.indices_char = json.loads(f.read())

    def _sample(self, preds, temperature=.6):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def predict(self, sentence, gen_chars=50):
        '''
        Generate text based on seed text.

        Args:
            sentence: Input seed text to kick off generation.
            gen_chars: How many characters of text to generate.

        Returns generated text
        '''

        # The model was trained on lowercase text only, and there is no
        # provision in the model itself for handling characters that are 
        # out of vocabulary.
        # To compensate, turn everything into lowercase, then check for
        # out-of-vocab characters in the result.
        sentence = sentence.lower()
        for t, char in enumerate(sentence):
            if char not in self.char_indices:
                print("Bad char {} at position {}".format(char, t))
                raise ValueError(
                        "Unexpected character '{}' at position {}. "
                        "Only lowercase ASCII characters, spaces, "
                        "and basic punctuation are supported.".format(char, t))

        # The text passed into the model must be exactly SEED_TEXT_LEN
        # characters long, or the model will crash. Pad or truncate.
        if len(sentence) > SEED_TEXT_LEN:
            sentence = sentence[:SEED_TEXT_LEN]
        else:
            sentence = sentence.rjust(SEED_TEXT_LEN)

        generated = ''
        with self.graph.as_default():
            for i in range(gen_chars):
                x = np.zeros((1, SEED_TEXT_LEN, self.num_chars))

                for t, char in enumerate(sentence):
                    x[0, t, self.char_indices[char]] = 1.

                preds = self.model.predict(x, verbose=0)[0]

                next_index = self._sample(preds)
                next_char = self.indices_char[str(next_index)]

                generated += next_char
                sentence = sentence[1:] + next_char

        return generated

