import json
from pickle import GET
from typing import override
from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import TaskSerializer
from .models import Task

# Create your views here.
#view.py  is the file that contains the views for the tasks app.
# A view is a function that takes a request and returns a response.

TASK_FILE = 'tasks/files/tasks.json'

class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=["GET"], url_path="completed")
    def get_only_completed_tasks(self, request):
        tasks = Task.objects.filter(completed=True)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], url_path="specific")
    def get_a_specific_task(self, request, pk=None):
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)