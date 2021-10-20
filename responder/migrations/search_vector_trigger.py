# Generated manually

from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_search_vector(apps, schema_editor):
    Question = apps.get_model("responder", "Question")
    Question.objects.update(search_vector=SearchVector("text"))


class Migration(migrations.Migration):

    dependencies = [
        ('responder', '0002_auto_20211020_0604'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER search_vector_trigger
                BEFORE INSERT OR UPDATE OF text, search_vector
                ON responder_question
                FOR EACH ROW EXECUTE PROCEDURE
                tsvector_update_trigger(
                    search_vector, 'pg_catalog.simple', text
                );
                UPDATE responder_question SET search_vector = NULL;
                """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS search_vector_trigger
                ON responder_question;
                """,
        ),
        migrations.RunPython(
            compute_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]
