from django_elasticsearch_dsl import Document, fields, DEDField, Field
from django_elasticsearch_dsl.registries import registry
from .models import Question


class DenseVector(DEDField, Field):
    name = 'dense_vector'

    def __init__(self, dims, attr=None, **kwargs):
        super(DenseVector, self).__init__(attr=attr, dims=dims, **kwargs)


@registry.register_document
class QuestionDocument(Document):
    embedding = DenseVector(512, attr='get_embedding')

    class Index:
        # Name of the Elasticsearch index
        name = 'questions'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Question # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'text',
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000