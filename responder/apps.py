from django.apps import AppConfig
import tensorflow_hub as hub
import tensorflow_text


class ResponderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'responder'

    neural_model = module = hub.load(
        'https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3'
    )

    def ready(self):
        import responder.signals
