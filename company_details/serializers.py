from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Employee, Contact, Payroll

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'city', 'phone_number', 'employee_code']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['address', 'phone', 'email']


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = ['salary']


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    contact = ContactSerializer()
    payroll = PayrollSerializer()

    class Meta:
        model = Employee
        fields = ['emp_num', 'designation', 'user', 'contact', 'payroll']

    def create(self, validated_data):
        from django.db import transaction

        try:
            with transaction.atomic():

                user_data = validated_data.pop('user')
                contact_data = validated_data.pop('contact')
                payroll_data = validated_data.pop('payroll')

                user = UserSerializer().create(user_data)

                employee = Employee.objects.create(
                    user=user,
                    emp_num=validated_data['emp_num'],
                    designation=validated_data['designation']
                )

                Contact.objects.create(employee=employee, **contact_data)
                Payroll.objects.create(employee=employee, **payroll_data)

                return employee

        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
