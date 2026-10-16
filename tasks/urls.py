from django.urls import path
from .views import add_numbers, get_tasks, get_task_by_id, create_task

urlpatterns = [
    path('add-numbers/', add_numbers), 
    path('get-all-tasks/', get_tasks), 
    path('get-task-by-id/<int:id>/', get_task_by_id),
    path('create-task/', create_task),
]