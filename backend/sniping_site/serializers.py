from rest_framework import serializers
from .models import *

#class showSerializer(serializers.ModelSerializer):
#    class Meta:
#        model=show
#        fields='__all__'

class theatreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Theatre
        fields=['location']

class playSerializer(serializers.ModelSerializer):
    class Meta:
        model=Play
        fields=['name']

class sectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Seat
        fields=['section']
