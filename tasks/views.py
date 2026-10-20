import json
from turtle import title
from typing import override
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.serializers import TaskSerializer
from .models import Task
# Create your views here.
#view.py  is the file that contains the views for the tasks app.
# A view is a function that takes a request and returns a response.

TASK_FILE = 'tasks/files/tasks.json'

class TaskView(APIView):

    #Get request to get task by id
    @override
    def get(self, request, id = None):
        try:
            if id is None:
                task = Task.objects.all()
                serilizer = TaskSerializer(task, many=True)
                serialized_data = serilizer.data
                return Response(data = serialized_data)
            
            else:
                task = Task.objects.get(id=id)
                serilizer = TaskSerializer(task)
                serialized_data = serilizer.data
                return Response(data = serialized_data)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=404)
    
    @override
    def post(self, request):
        try:
            data = request.data
            serializer = TaskSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) #201 is the status code for created
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @override
    def put(self, request, id=None):
        if id is None:
            return Response({'error': 'Task id is required'}, status=400)
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task, data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=404)
        

    @override
    def delete(self, request, id=None):
        if id is None:
            return Response({'error': 'Task id is required'}, status=400)
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=404)