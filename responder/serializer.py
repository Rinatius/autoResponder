from rest_framework import serializers

from responder import models


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = "__all__"


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Campaign
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()
    campaign = CampaignSerializer()

    class Meta:
        model = models.Answer
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer()
    language = LanguageSerializer()
    campaign = CampaignSerializer()

    class Meta:
        model = models.Question
        fields = "__all__"
