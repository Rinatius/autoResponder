from elasticsearch_dsl import Q
from rest_framework import filters
from django.utils.translation import gettext_lazy as _

from responder.models import Answer
from responder.services import utils
from responder import documents, exceptions, serializer
from responder.apps import ResponderConfig
import tensorflow as tf


class ElasticSearchFilter(filters.SearchFilter):
    serializer_class = None
    document_class = None

    search_param = "elastic"
    search_title = _("Elastic Search")

    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""
        pass

    def generate_search(self, document_class, query):
        language = utils.detect_language(query)
        query_expression = self.generate_q_expression(query)
        search = (
            self.document_class.search()
            .filter("term", language__short_name=language)
            .query(query_expression)
        )

        return search

    def get_search_terms(self, request):
        """
        Search term is set by a ?search=... query parameter.
        """
        params = request.query_params.get(self.search_param, "")
        params = params.replace("\x00", "")  # strip null characters
        params = params.replace(",", " ")
        return params

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_term = self.get_search_terms(request)

        if not search_fields or not search_term:
            return queryset

        search = self.generate_search(self.document_class, search_term)[:3]
        results = search.execute()

        response = search.to_queryset()
        if self.document_class == documents.AnswerDocument:
            answer_options = [answer.english_text for answer in response]
            best_answer = utils.generate_best_response(
                utils.translate_text(search_term), answer_options
            )
            if best_answer != -1:
                response = Answer.objects.filter(pk=response[best_answer].id)
            else:
                raise exceptions.NoAnswerToTheQuestionException

        return response


class QuestionElasticSearchFilter(ElasticSearchFilter):
    serializer_class = serializer.QuestionListSerializer
    document_class = documents.QuestionDocument

    def generate_q_expression(self, query):
        return Q("multi_match", query=query, fields=["text"], fuzziness="auto")


class QuestionCosineElasticSearchFilter(ElasticSearchFilter):
    search_param = "cosine"
    search_title = _("Cosine Elastic Search")

    serializer_class = serializer.QuestionListSerializer
    document_class = documents.QuestionDocument

    def generate_q_expression(self, query):
        query = utils.translate_text(query)

        if not utils.is_question(query):
            raise exceptions.NotAQuestionException(_("Input is not a question"))

        vector = ResponderConfig.neural_model.signatures["question_encoder"](
            tf.constant(
                [
                    query,
                ]
            )
        )
        vector = list(vector["outputs"].numpy()[0])
        q = Q(
            "function_score",
            script_score={
                "script": {
                    "source": "cosineSimilarity(params.queryVector, 'embedding') + 1.0",
                    "params": {"queryVector": vector},
                }
            },
        )
        return q

    def filter_queryset(self, request, queryset, view):
        try:
            return super().filter_queryset(request, queryset, view)
        except exceptions.NotAQuestionException:
            raise exceptions.NotAQuestionException


class AnswerCosineElasticSearchFilter(QuestionCosineElasticSearchFilter):
    serializer_class = serializer.AnswerListSerializer
    document_class = documents.AnswerDocument
