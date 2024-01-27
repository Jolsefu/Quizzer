from rest_framework import serializers
from .models import QuizFile


class QuizFileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = QuizFile
        fields = ["user", "file"]
