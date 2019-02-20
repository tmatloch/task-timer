
from rest_framework import serializers
from .models import Task, Entry, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('url', 'username', 'email')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry