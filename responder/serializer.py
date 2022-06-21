from rest_framework import serializers

from responder.models import Campaign, Answer, Question, Article, Image, ImageAnswer


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
    article = ArticleSerializer(read_only=True)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ImageAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAnswer
        fields = '__all__'