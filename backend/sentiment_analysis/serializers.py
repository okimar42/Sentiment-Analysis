from rest_framework import serializers

from django.contrib.auth.models import User

from .models import ImageSentimentResult, SentimentAnalysis, SentimentResult


class ImageSentimentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSentimentResult
        fields = [
            "image_url",
            "image_description",
            "score",
            "gpt4_vision_score",
            "claude_vision_score",
            "gemini_vision_score",
            "created_at",
        ]


class SentimentResultSerializer(serializers.ModelSerializer):
    image_results = ImageSentimentResultSerializer(many=True, read_only=True)
    score = serializers.SerializerMethodField()

    def get_score(self, obj):
        return obj.final_score

    class Meta:
        model = SentimentResult
        fields = [
            "id",
            "post_id",
            "content",
            "score",
            "compound_score",
            "created_at",
            "has_images",
            "vader_score",
            "gpt4_score",
            "claude_score",
            "gemini_score",
            "grok_score",
            "sarcasm_score",
            "is_sarcastic",
            "perceived_iq",
            "bot_probability",
            "is_bot",
            "post_date",
            "image_results",
            "source_type",
        ]


class SentimentAnalysisSerializer(serializers.ModelSerializer):
    results = SentimentResultSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    source = serializers.ListField(
        child=serializers.ChoiceField(
            choices=[c[0] for c in SentimentAnalysis.SOURCE_CHOICES]
        ),
        help_text='List of sources (e.g. ["reddit", "twitter"])',
        allow_empty=False,
    )

    class Meta:
        model = SentimentAnalysis
        fields = [
            "id",
            "user",
            "query",
            "source",
            "model",
            "subreddits",
            "start_date",
            "end_date",
            "status",
            "created_at",
            "updated_at",
            "results",
            "include_images",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]


class SentimentAnalysisCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    source = serializers.ListField(
        child=serializers.ChoiceField(
            choices=[c[0] for c in SentimentAnalysis.SOURCE_CHOICES]
        ),
        help_text='List of sources (e.g. ["reddit", "twitter"])',
        allow_empty=False,
    )

    class Meta:
        model = SentimentAnalysis
        fields = [
            "id",
            "query",
            "source",
            "model",
            "selected_llms",
            "subreddits",
            "start_date",
            "end_date",
            "include_images",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email already exists.")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user
