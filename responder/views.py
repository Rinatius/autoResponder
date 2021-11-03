import abc

from django.contrib.admin.utils import unquote
from django.shortcuts import render
from elasticsearch_dsl import Q
from rest_framework import viewsets, filters
from rest_framework.response import Response

from responder.apps import ResponderConfig
from responder.documents import QuestionDocument, AnswerDocument
from responder.models import Campaign, Answer, Question
from responder.serializer import CampaignSerializer, AnswerSerializer, QuestionSerializer
from django.utils.translation import gettext_lazy as _
import tensorflow as tf


# class FullTextQuestionSearchFilter(filters.BaseFilterBackend):
#     """Query Questions on the basis of `search` query param."""
#
#     def filter_queryset(self, request, queryset, view):
#         search_term = request.query_params.get("search", None)
#         if search_term:
#             search_term = unquote(search_term)
#             # We use the computed `search_vector` directly
#             # to speed up the search.
#             return queryset.filter(search_vector=search_term)
#
#         return queryset


class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()


class ElasticSearchFilter(filters.SearchFilter):
    serializer_class = None
    document_class = None

    search_param = "elastic"
    search_title = _('Elastic Search')

    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""
        pass

    def generate_search(self, document_class, query):
        query_expression = self.generate_q_expression(query)
        search = self.document_class.search().query(query_expression)
        return search

    def get_search_terms(self, request):
        """
        Search term is set by a ?search=... query parameter.
        """
        params = request.query_params.get(self.search_param, '')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        return params

    def filter_queryset(self, request, queryset, view):
        print("Getting search results!!!")

        search_fields = self.get_search_fields(view, request)
        search_term = self.get_search_terms(request)

        if not search_fields or not search_term:
            return queryset

        # q = self.generate_q_expression(search_term)
        # search = self.document_class.search().query(q)
        search = self.generate_search(self.document_class, search_term)[:3]
        print("SEARCH results")
        results = search.execute()
        print(results)
        for hit in results:
            print(hit.meta.score)
        response = search.to_queryset()
        print("Elastic search complete!!!")

        #queryset = queryset.intersection(response)
        return response


class QuestionElasticSearchFilter(ElasticSearchFilter):
    serializer_class = QuestionSerializer
    document_class = QuestionDocument

    def generate_q_expression(self, query):
        print("Generating Q expression!!!")
        return Q(
            'multi_match',
            query=query,
            fields=['text'],
            fuzziness='auto')


class QuestionCosineElasticSearchFilter(ElasticSearchFilter):
    search_param = "cosine"
    search_title = _('Cosine Elastic Search')

    serializer_class = QuestionSerializer
    document_class = QuestionDocument

    def generate_q_expression(self, query):
        vector = ResponderConfig.neural_model.signatures['question_encoder'](
            tf.constant([query, ]))
        vector = list(vector['outputs'].numpy()[0])
        q = Q("function_score",
              # query=Q(
              #     'bool',
              #     must=[
              #         Q('match', test='a'),
              #     ]),
              script_score={"script": {
                  "source": "cosineSimilarity(params.queryVector, 'embedding') + 1.0",
                  "params": {
                      "queryVector": vector
                  }
              }},
              )
        return q

# class QuestionEuclideanElasticSearchFilter(ElasticSearchFilter):
#     search_param = "euclidean"
#     search_title = _('Euclidean Elastic Search')
#
#     serializer_class = QuestionSerializer
#     document_class = QuestionDocument
#
#     def generate_q_expression(self, query):
#         vector = ResponderConfig.neural_model.signatures['question_encoder'](
#             tf.constant([query, ]))
#         vector = list(vector['outputs'].numpy()[0])
#         q = Q("function_score",
#               # query=Q(
#               #     'bool',
#               #     must=[
#               #         Q('match', test='a'),
#               #     ]),
#               script_score={"script": {
#                   "source": "1 / (1 + l1norm(params.queryVector, 'embedding'))",
#                   "params": {
#                       "queryVector": vector
#                   }
#               }},
#               )
#         return q

class AnswerCosineElasticSearchFilter(QuestionCosineElasticSearchFilter):
    serializer_class = AnswerSerializer
    document_class = AnswerDocument


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['text']
    filter_backends = [QuestionCosineElasticSearchFilter, filters.SearchFilter, QuestionElasticSearchFilter]
    search_fields = ['text']


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    filter_backends = [AnswerCosineElasticSearchFilter, ]
    search_fields = ['text']

# class ElasticSearchViewSet(viewsets.ViewSet):
#     serializer_class = None
#     document_class = None
#
#     @abc.abstractmethod
#     def generate_q_expression(self, query):
#         """This method should be overridden
#         and return a Q() expression."""
#
#     def get(self, request, query):
#         try:
#             q = self.generate_q_expression(query)
#             search = self.document_class.search().query(q)
#             response = search.execute()
#
#             print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')
#
#             results = self.paginate_queryset(response, request, view=self)
#             serializer = self.serializer_class(results, many=True)
#             return self.get_paginated_response(serializer.data)
#         except Exception as e:
#             return HttpResponse(e, status=500)
