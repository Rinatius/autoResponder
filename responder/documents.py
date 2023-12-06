from django_elasticsearch_dsl import Document, fields, DEDField, Field
from django_elasticsearch_dsl.registries import registry
from .models import Question, Answer, Language


class DenseVector(DEDField, Field):
    name = "dense_vector"

    def __init__(self, dims, attr=None, **kwargs):
        super(DenseVector, self).__init__(attr=attr, dims=dims, **kwargs)


@registry.register_document
class QuestionDocument(Document):
    embedding = DenseVector(512, attr="get_embedding")

    language = fields.ObjectField(
        properties={
            "name": fields.TextField(),
            "short_name": fields.TextField(),
        }
    )

    class Index:
        # Name of the Elasticsearch index
        name = "questions"
        # See Elasticsearch Indices API reference for available settings
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Question  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            "text",
        ]

        related_models = [Language]


    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Language):
            return related_instance.answers.all()

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000


@registry.register_document
class AnswerDocument(Document):
    embedding = DenseVector(512, attr="get_embedding")

    language = fields.ObjectField(
        properties={
            "name": fields.TextField(),
            "short_name": fields.TextField(),
        }
    )

    class Index:
        # Name of the Elasticsearch index
        name = "answers"
        # See Elasticsearch Indices API reference for available settings
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Answer  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            "text",
        ]
        related_models = [Language]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Language):
            return related_instance.answers.all()
