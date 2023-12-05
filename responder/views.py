from rest_framework import viewsets, filters

from responder.models import Campaign, Answer, Question
from responder.serializer import (
    AnswerSerializer,
    CampaignSerializer,
    QuestionSerializer,
)
from responder.services.elasticsearch import (
    AnswerCosineElasticSearchFilter,
    QuestionCosineElasticSearchFilter,
    QuestionElasticSearchFilter,
)


class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()


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
