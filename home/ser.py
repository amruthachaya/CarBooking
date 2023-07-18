from rest_framework import serializers

from home.models import Tracking


class GpsTracker(serializers.ModelSerializer):
    device_id = serializers.IntegerField(default=1)
    timestamp = serializers.IntegerField(default=111111)
    lat = serializers.FloatField(default=0.0)
    lon = serializers.FloatField(default=0.0)
    speed = serializers.FloatField(default=0.0)
    bearing = serializers.FloatField(default=0.0)
    altitude = serializers.FloatField(default=0.0)
    accuracy = serializers.FloatField(default=0.0)
    batt = serializers.FloatField(default=0.0)
    charge = serializers.BooleanField(default=False)

    class Meta:
        model = Tracking
        fields = "__all__"
