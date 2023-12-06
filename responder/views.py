from rest_framework import viewsets, filters

from responder import models, serializer
from responder.services import utils, elasticsearch


class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.CampaignSerializer
    queryset = models.Campaign.objects.all()


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.QuestionListSerializer
    queryset = models.Question.objects.all()
    filter_backends = [
        elasticsearch.QuestionCosineElasticSearchFilter,
        filters.SearchFilter,
        elasticsearch.QuestionElasticSearchFilter,
    ]
    search_fields = ["text"]

    def get_serializer_class(self):
        if self.action == "create":
            return serializer.AnswerCreateSerializer
        return serializer.AnswerListSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    filter_backends = [
        elasticsearch.AnswerCosineElasticSearchFilter,
    ]
    search_fields = ["text"]

    def get_serializer_class(self):
        if self.action == "create":
            return serializer.QuestionCreateSerializer
        return serializer.QuestionListSerializer

    def perform_create(self, serializer):
        text = serializer.validated_data["text"]
        language = utils.detect_language(text)
        language = models.Language.objects.get(short_name=language)
        serializer.save(language=language)
