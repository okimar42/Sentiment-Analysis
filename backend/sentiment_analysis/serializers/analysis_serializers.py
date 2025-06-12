from rest_framework import serializers

from ..models import SentimentResult


class SentimentResultSerializer(serializers.ModelSerializer):
    grok_score = serializers.FloatField(required=False, allow_null=True, default=None)

    class Meta:
        model = SentimentResult
        fields = "__all__"
