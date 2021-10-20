from django.contrib.admin.utils import unquote
from django.shortcuts import render
from rest_framework import viewsets, filters

from responder.models import Campaign, Answer, Question
from responder.serializer import CampaignSerializer, AnswerSerializer, QuestionSerializer


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


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['text']
