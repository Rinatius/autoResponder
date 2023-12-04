import tensorflow as tf

# import numpy as np
from django.db import models

from responder.apps import ResponderConfig
from responder.services.utils import translate_text


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
        Campaign, on_delete=models.CASCADE, related_name="topics", help_text="Campaign"
    )

    def __str__(self):
        return self.name


class Answer(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="answers", help_text="Campaign"
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,  # TODO Change deletion model
        related_name="answers",
        help_text="Language",
    )
    text = models.TextField()
    english_text = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.english_text:
            self.english_text = translate_text(self.text)

        super().save(*args, **kwargs)

    def get_embedding(self):
        answer_context = self.english_text.split(". ", 1)
        answer = answer_context[0]
        if len(answer_context) > 1:
            context = answer_context[1]
        else:
            context = answer_context[0]

        answer = translate_text(answer)
        context = translate_text(context)

        embeddings = ResponderConfig.neural_model.signatures["response_encoder"](
            input=tf.constant(
                [
                    answer,
                ]
            ),
            context=tf.constant(
                [
                    context,
                ]
            ),
        )
        return list(embeddings["outputs"].numpy()[0])

    def __str__(self):
        return self.text


class Question(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="questions",
        help_text="Campaign",
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,  # TODO Change deletion model
        related_name="questions",
        help_text="Language",
    )
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name="questions", help_text="Answer"
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,  # TODO Change deletion model
        related_name="questions",
        help_text="Topic",
    )
    text = models.TextField()

    # search_vector = SearchVectorField(null=True, blank=True)
    #
    # class Meta:
    #     indexes = (GinIndex(fields=["search_vector"]),)

    def get_embedding(self):
        embeddings = ResponderConfig.neural_model.signatures["question_encoder"](
            tf.constant(
                [
                    self.text,
                ]
            )
        )
        return list(embeddings["outputs"].numpy()[0])

    def __str__(self):
        return self.text
