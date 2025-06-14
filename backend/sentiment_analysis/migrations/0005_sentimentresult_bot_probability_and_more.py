# Generated by Django 5.2.1 on 2025-05-25 17:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment_analysis', '0004_sentimentresult_is_sarcastic_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='sentimentresult',
            name='bot_probability',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='is_bot',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='manual_override',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='manual_sentiment',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='override_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='override_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='override_reason',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='perceived_iq',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='post_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='source_metadata',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='sentimentresult',
            name='source_type',
            field=models.CharField(default='reddit', max_length=50),
        ),
        migrations.AddIndex(
            model_name='sentimentresult',
            index=models.Index(fields=['post_date'], name='sentiment_a_post_da_9650ba_idx'),
        ),
        migrations.AddIndex(
            model_name='sentimentresult',
            index=models.Index(fields=['perceived_iq'], name='sentiment_a_perceiv_766eda_idx'),
        ),
        migrations.AddIndex(
            model_name='sentimentresult',
            index=models.Index(fields=['bot_probability'], name='sentiment_a_bot_pro_cb2d20_idx'),
        ),
        migrations.AddIndex(
            model_name='sentimentresult',
            index=models.Index(fields=['source_type'], name='sentiment_a_source__75fadf_idx'),
        ),
    ]
