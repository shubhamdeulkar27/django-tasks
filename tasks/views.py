import json
from typing import override
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
#view.py  is the file that contains the views for the tasks app.
# A view is a function that takes a request and returns a response.

TASK_FILE = 'tasks/files/tasks.json'

class TaskView(APIView):

    def __get_all_tasks(self):
        with open(TASK_FILE, 'r') as file:
            return json.loads(file.read())

    #Get request to get task by id
    @override
    def get(self, request, id = None):
        tasks = self.__get_all_tasks()
        if id is None:
            return Response({'tasks': tasks})
        for task in tasks:
            if task['id'] == id:
                return Response({'task': task})
        return Response({'error': 'Task not found'}, status=404)
    
    @override
    def post(self, request):
        #get the task from the request body
        data = request.data
        #add the task to the json file
        tasks = self.__get_all_tasks()
        task = {
            'id': len(tasks) + 1,
            'title': data['title'],
            'description': data['description'],
            'completed': False
        }
        with open(TASK_FILE,'w') as file:
            tasks.append(task)
            json.dump(tasks, file)
        return Response(task,status=status.HTTP_201_CREATED) #201 is the status code for created

    @override
    def put(self, request, id=None):
        if id is None:
            return Response({'error': 'Task id is required'}, status=400)
        tasks = self.__get_all_tasks()
        data = request.data
        for task in tasks:
            if task['id'] == id:
                task['title'] = data.get('title', task['title'])
                task['description'] = data.get('description', task['description'])
                task['completed'] = data.get('completed', task['completed'])
                with open(TASK_FILE, 'w') as file:
                    json.dump(tasks, file)
                return Response({'task': task})
        return Response({'error': 'Task not found'}, status=404)

    @override
    def delete(self, request, id=None):
        if id is None:
            return Response({'error': 'Task id is required'}, status=400)
        tasks = self.__get_all_tasks()
        updated_tasks = [task for task in tasks if task['id'] != id]
        if len(updated_tasks) == len(tasks):
            return Response({'error': 'Task not found'}, status=404)
        with open(TASK_FILE, 'w') as file:
            json.dump(updated_tasks, file)
        return Response(status=status.HTTP_204_NO_CONTENT)