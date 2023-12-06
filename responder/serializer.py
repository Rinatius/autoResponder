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


class AnswerListSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()
    campaign = CampaignSerializer()

    class Meta:
        model = models.Answer
        fields = "__all__"


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = "__all__"

    @staticmethod
    def validate_text(value):
        if models.Answer.objects.filter(text__iexact=value).exists():
            raise serializers.ValidationError(
                "An answer with this text already exists."
            )
        return value


class QuestionListSerializer(serializers.ModelSerializer):
    answer = AnswerListSerializer()
    language = LanguageSerializer()
    campaign = CampaignSerializer()

    class Meta:
        model = models.Question
        fields = "__all__"


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = "__all__"

    @staticmethod
    def validate_text(value):
        if models.Question.objects.filter(text__iexact=value).exists():
            raise serializers.ValidationError(
                "An question with this text already exists."
            )
        return value
