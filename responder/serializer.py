from rest_framework import serializers

from responder.models import Campaign, Answer, Question


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer()

    class Meta:
        model = Question
        fields = ["id", "text", "campaign", "language", "answer", "topic"]
