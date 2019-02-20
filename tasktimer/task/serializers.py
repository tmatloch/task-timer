
from rest_framework import serializers
from .models import Task, Entry, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('url', 'username', 'email')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'owner', 'name', 'start_date_time', 'end_date_time', 'is_finished', 'is_running', 'duration')

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('id', 'task', 'start_date_time', 'end_date_time', 'is_finished')
