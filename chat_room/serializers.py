from rest_framework import serializers
from chat_room.models import Consultant

__author__ = 'Piotr'

class ConsultantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consultant
        fields = ('id', 'name', 'password', 'google_id', 'is_available')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.google_id = validated_data.get('google_id', instance.google_id)
        instance.is_available = validated_data.get('is_available', instance.is_available)
        instance.save()
        return instance

