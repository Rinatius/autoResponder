import datetime
import os.path

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import tensorflow_text
import cv2
import face_recognition
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

    img_path = '{:media/%Y/%m/%d/}'.format(datetime.datetime.now())
    image = models.ImageField(upload_to=img_path)

    def get_embedding(self):
        img = cv2.imread(self.image.path)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encoding = list(face_recognition.face_encodings(rgb_img, model='large')[0])
        face_locations = face_recognition.face_locations(rgb_img)
        for number, face_location in enumerate(face_locations):
            y1, x2, y2, x1 = face_location[0], face_location[1], face_location[2], face_location[3]
            crop_img = img[y1:y2, x1:x2]
            cv2.imwrite(self.image.path, crop_img)
            return img_encoding


class ImageAnswer(models.Model):
    img_path = '{:mediaAnswer/%Y/%m/%d/}'.format(datetime.datetime.now())
    image = models.ImageField(upload_to=img_path)

