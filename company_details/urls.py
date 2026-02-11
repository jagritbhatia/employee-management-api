from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_employee),
    path('employees/', views.get_all_employees),
    path('employee/<str:emp_num>/', views.get_employee),
    path('top-employees/', views.get_top_employees),
    path('increment-salary/', views.increment_salary),
]
