from rest_framework import serializers

from home.models import Tracking


class GpsTracker(serializers.ModelSerializer):
    device_id = serializers.IntegerField()
    timestamp = serializers.IntegerField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    speed = serializers.FloatField()
    bearing = serializers.FloatField()
    altitude = serializers.FloatField()
    accuracy = serializers.FloatField()
    batt = serializers.FloatField()
    charge = serializers.BooleanField()

    class Meta:
        model = Tracking
        fields = "__all__"
