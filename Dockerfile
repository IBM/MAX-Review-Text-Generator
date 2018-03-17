FROM floydhub/dl-base:2.1.0-py3.22

ARG model_bucket=http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/keras/generative_lang_model
ARG model_file=generative_lang_model.h5

WORKDIR /workspace
RUN mkdir assets
RUN wget -nv ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file}

# Python package versions
ARG numpy_version=1.14.1
ARG tf_version=1.5.0
ARG keras_version=2.1.4

RUN pip install --upgrade pip && \
	pip install numpy==${numpy_version} && \
    pip install tensorflow==${tf_version} && \
    pip install h5py && \
    pip install keras==${keras_version} && \
    pip install flask-restplus

COPY . /workspace

EXPOSE 5000

CMD python app.py