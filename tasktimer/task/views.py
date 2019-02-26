import pytz

from datetime import timedelta, datetime, timezone

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
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
        tasks = map(recalculation_needed, tasks)
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


@api_view(['GET', 'PATCH', 'DELETE'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        task = recalculation_needed(task)
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PATCH':
        data = request.data
        is_running = data.get("is_running")
        if(is_running != None):
            if(is_running):
                create_entry(task)
                recalculate_duration(task)
            else:
                running_entry=Entry.objects.filter(task=task.id, end_date_time=None).last()
                close_entry(running_entry)
                recalculate_duration(task)
        is_finished = data.get("is_finished")
        if(is_finished !=None):
            if(is_finished):
                finished_task(task)
                running_entry=Entry.objects.filter(task=task.id, end_date_time=None).last()
                if(running_entry!= None):
                    close_entry(running_entry)
                    recalculate_duration(task)
        serializer = TaskSerializer(task, data=data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        Task.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)


def create_entry(task):
    now_date = datetime.now().isoformat()
    entry = Entry.objects.create(task=task, start_date_time=now_date)

def close_entry(entry):
    now_date = datetime.now().isoformat()
    entry.end_date_time=now_date
    entry.is_finished=True
    entry.save()

def recalculate_duration(task):
    task_entries=Entry.objects.filter(task=task.id)
    duration_list = map(calculate_entry, task_entries)
    duration = sum(duration_list, timedelta(0))
    task.duration = duration
    task.save()

def calculate_entry(entry):
    start_date_time = entry.start_date_time
    end_date_time = entry.end_date_time
    if(end_date_time == None):
        offset = pytz.timezone("Europe/Warsaw")
        end_date_time = datetime.now(timezone.utc) + offset.utcoffset(datetime.now())
    duration = end_date_time - start_date_time
    return duration - timedelta(microseconds=duration.microseconds)

def recalculation_needed(task):
    not_finished_task = Entry.objects.filter(task=task.id, is_finished=False).last()
    if(not_finished_task == None):
        return task
    else:
        recalculate_duration(task)
        return task


def finished_task(task):
    now_date = datetime.now().isoformat()
    task.is_running = False
    task.end_date_time=now_date
    task.save()


@api_view(['GET'])
def entry_list(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        task_entries = Entry.objects.filter(task=task)
        serializer = EntrySerializer(task_entries, many=True)
        return JsonResponse(serializer.data, safe=False)

