import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta

# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.email

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=255)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField(blank=True, null=True)
    is_running = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    duration = models.DurationField(default=timedelta(seconds=0))

class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)

    class Meta:
        ordering = ('start_date_time',)



