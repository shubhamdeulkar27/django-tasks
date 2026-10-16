import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
#view.py  is the file that contains the views for the tasks app.
# A view is a function that takes a request and returns a response.

@api_view(['GET'])
def add_numbers(request):
    #get the numbers from the request query parameters
    try:
        a = request.query_params['a']
        b = request.query_params['b']
        #convert the numbers to integers
        a = int(a)
        b = int(b)
        #add the numbers
        result = a + b
        return Response({'Sum': result})
    except:
        print("Invalid numbers")
        return Response({'error': 'Invalid numbers'}, status=400)

#**************************Tasks API********************************

TASK_FILE = 'tasks/files/tasks.json'

@api_view(['GET'])
def get_tasks(request):
    #get the tasks from the json file
    with open(TASK_FILE, 'r') as file:
        tasks = json.load(file)
    return Response({'tasks': tasks})

@api_view(['GET'])
def get_task_by_id(request, id):
    #get the task from the json file
    with open(TASK_FILE, 'r') as file:
        tasks = json.load(file)
    for task in tasks:
        if task['id'] == id:
            return Response({'task': task})
    return Response({'error': 'Task not found'}, status=404)


# @api_view(['POST'])
# def create_task(request):
#     #get the task from the request body
#     data = request.data
#     #add the task to the json file
#     with open(TASK_FILE,'r') as file:
#         tasks = json.load(file)
#     task = {
#             'id': len(tasks) + 1,
#             'title': data['title'],
#             'description': data['description'],
#             'completed': False
#         }
#     with open(TASK_FILE,'w') as file:
#         tasks.append(task)
#         json.dump(tasks, file)
#     return Response(task,status=status.HTTP_201_CREATED) #201 is the status code for created 


class TaskView(APIView):

    def create(self, request):
        #get the task from the request body
        data = request.data
        #add the task to the json file
        with open(TASK_FILE,'r') as file:
            tasks = json.load(file)
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