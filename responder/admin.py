from django.contrib import admin

# Register your models here.
from responder.models import Campaign, Language, Topic, Answer, Question, Article, Image


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('search_vector', 'answer__text', 'text')


admin.site.register(Campaign)
admin.site.register(Language)
admin.site.register(Topic)
admin.site.register(Answer)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Article)
admin.site.register(Image)
