from .models import BaseballStats
from rest_framework import serializers

class BaseballStatsSerializer(serializers.ModelSerializer):
    # return the human-readable text value corresponding to the choice value stored in the database for the "bats" field,
    #  e.g. "Left", "Right", "Both"
    bats = serializers.CharField(source='get_bats_display')

    class Meta:
        model = BaseballStats
        # all model fields shortcut
        fields = "__all__"

class PlayerDescriptionSerializer(serializers.Serializer):
    player = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)

