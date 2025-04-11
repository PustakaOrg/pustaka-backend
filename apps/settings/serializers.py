from rest_framework import serializers
from .models import Settings

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['max_loan_day', 'fine_per_lateday', 'fine_for_lost']
