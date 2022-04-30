import tensorflow as tf
import tensorflow_hub as hub
# import numpy as np
import tensorflow_text
from django.db import models

from responder.apps import ResponderConfig


class Language(models.Model):
    name = models.CharField(max_length=400)
    short_name = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=400)
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="topics",
        help_text="Campaign"
    )

    def __str__(self):
        return self.name


class Article(models.Model):
    header = models.TextField()
    lid = models.TextField(blank=True, null=True)
    url = models.URLField()
    text = models.TextField()
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="article",
        help_text="Campaign"
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="article",
        help_text="Language"
    )

    def __str__(self):
        return self.text


class Answer(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="answers",
        help_text="Campaign"
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,  # TODO Change deletion model
        related_name="answers",
        help_text="Language"
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="answers",
        help_text="Article",
        blank=True,
        null=True
    )
    url = models.URLField(blank=True, null=True)
    text = models.TextField()

    def get_embedding(self):
        answer_context = self.text.split('. ', 1)
        answer = answer_context[0]
        if len(answer_context) > 1:
            context = answer_context[1]
        else:
            context = answer_context[0]

        embeddings = ResponderConfig.neural_model.signatures['response_encoder'](
            input=tf.constant([answer, ]),
            context=tf.constant([context, ]))
        return list(embeddings['outputs'].numpy()[0])

    def __str__(self):
        return self.text


class Question(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="questions",
        help_text="Campaign"
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,  # TODO Change deletion model
        related_name="questions",
        help_text="Language"
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="questions",
        help_text="Answer"
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,  # TODO Change deletion model
        related_name="questions",
        help_text="Topic"
    )
    text = models.TextField()
    # search_vector = SearchVectorField(null=True, blank=True)
    #
    # class Meta:
    #     indexes = (GinIndex(fields=["search_vector"]),)

    def get_embedding(self):
        embeddings = ResponderConfig.neural_model.signatures['question_encoder'](
            tf.constant([self.text, ]))
        return list(embeddings['outputs'].numpy()[0])

    def __str__(self):
        return self.text


class Image(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Campaign"
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Topic"
    )
    image = models.ImageField(upload_to='media/% Y/% m/% d/')