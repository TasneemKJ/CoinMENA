from rest_framework import serializers
from .models import Rate


class RateSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=3)

    exchange_rate = serializers.FloatField()
    pid_price = serializers.FloatField()
    ask_price = serializers.FloatField()

    class Meta:
        model = Rate
        fields = '__all__'
