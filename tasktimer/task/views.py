from datetime import timedelta, datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Task, Entry, CustomUser
from .serializers import TaskSerializer, EntrySerializer, UserSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def task(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(owner=request.user).order_by("start_date_time")
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = request.data
        data['owner'] = request.user.id
        data['start_date_time'] = datetime.now().isoformat()
        serializer = TaskSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
