from rest_framework import status
from rest_framework.exceptions import APIException


class NotAQuestionException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Is not a question"


class NoAnswerToTheQuestionException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No answer to the question"
