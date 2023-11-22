from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("responder", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="english_text",
            field=models.TextField(blank=True, null=True),
        ),
    ]
