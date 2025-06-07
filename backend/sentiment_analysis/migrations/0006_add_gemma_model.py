from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('sentiment_analysis', '0005_sentimentresult_bot_probability_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentimentanalysis',
            name='model',
            field=models.CharField(
                choices=[
                    ('vader', 'VADER'),
                    ('gpt4', 'GPT-4'),
                    ('claude', 'Claude'),
                    ('gemini', 'Gemini'),
                    ('gemma', 'Gemma'),
                    ('grok', 'Grok'),
                ],
                default='vader',
                max_length=10
            ),
        ),
    ] 