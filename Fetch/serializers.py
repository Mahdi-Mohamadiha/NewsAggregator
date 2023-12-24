from .models import Archive
from rest_framework import serializers

class ArchiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Archive
        fields = '__all__'
        