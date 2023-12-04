from rest_framework import viewsets, filters

from responder.documents import AnswerDocument
from responder.models import Campaign, Answer, Question
from responder.serializer import (
    CampaignSerializer,
    AnswerSerializer,
    QuestionSerializer,
)
from responder.services.elasticsearch import (
    QuestionCosineElasticSearchFilter,
    QuestionElasticSearchFilter,
)


class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()


class AnswerCosineElasticSearchFilter(QuestionCosineElasticSearchFilter):
    serializer_class = AnswerSerializer
    document_class = AnswerDocument


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    filter_backends = [
        QuestionCosineElasticSearchFilter,
        filters.SearchFilter,
        QuestionElasticSearchFilter,
    ]
    search_fields = ["text"]


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    filter_backends = [
        AnswerCosineElasticSearchFilter,
    ]
    search_fields = ["text"]
