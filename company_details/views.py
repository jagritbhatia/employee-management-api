from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Employee, Payroll
from .serializers import EmployeeSerializer


# 1️⃣ Register API
@api_view(['POST'])
def register_employee(request):
    serializer = EmployeeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Employee created successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2️⃣ Get All Employees
@api_view(['GET'])
def get_all_employees(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 3️⃣ Get Specific Employee
@api_view(['GET'])
def get_employee(request, emp_num):
    employee = get_object_or_404(Employee, emp_num=emp_num)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 4️⃣ Get High Salary Employees
@api_view(['GET'])
def get_top_employees(request):
    employees = Employee.objects.filter(payroll__salary__gt=10000)
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 5️⃣ Salary Increment API (Protected)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def increment_salary(request):
    emp_num = request.data.get('emp_num')

    if not emp_num:
        return Response(
            {"error": "emp_num is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    employee = get_object_or_404(Employee, emp_num=emp_num)

    payroll = get_object_or_404(Payroll, employee=employee)

    try:
        with transaction.atomic():

            if payroll.salary < 10000:
                payroll.salary += 2000
            else:
                payroll.salary += 5000

            payroll.save()

        return Response(
            {"message": "Salary updated successfully", "new_salary": payroll.salary},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
