from django.apps import AppConfig
import tensorflow_hub as hub
import tensorflow_text


class ResponderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'responder'

    neural_model = module = hub.load(
        'responder/neuralnetworks/universal-sentence-encoder-multilingual-qa_3/'
    )
