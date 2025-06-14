# Generated by Django 5.2.1 on 2025-05-25 01:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment_analysis', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagesentimentresult',
            name='confidence',
        ),
        migrations.RemoveField(
            model_name='imagesentimentresult',
            name='dominant_emotion',
        ),
        migrations.AddField(
            model_name='imagesentimentresult',
            name='claude_vision_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='imagesentimentresult',
            name='gemini_vision_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='imagesentimentresult',
            name='gpt4_vision_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='claude_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='gemini_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='gpt4_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='vader_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='imagesentimentresult',
            name='image_description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='sentimentanalysis',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sentimentanalysis',
            name='include_images',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sentimentanalysis',
            name='source',
            field=models.CharField(choices=[('reddit', 'Reddit'), ('twitter', 'Twitter')], default='reddit', max_length=50),
        ),
        migrations.AlterField(
            model_name='sentimentanalysis',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sentimentanalysis',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
    ]
