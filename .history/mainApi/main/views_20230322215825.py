from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from main.serializers import CreateCustomerAddressSerializer, CreateCarSerializer
from django.db import connections
from datetime import datetime
import re
# Create your views here.


def validate_email(email):
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False


class CustomeRegisterView(APIView):
    def post(self, request, format=None):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        age = request.data.get('age')
        date_of_birth = request.data.get('date_of_birth')
        phone = request.data.get('phone')
        email = request.data.get('email')
        format = "%Y-%d-%m"
        res = True
        try:
            res = bool(datetime.strptime(request.POST.get('date_of_birth'), format))
        except ValueError:
            res = False
        try:
            if first_name == '':
                return Response({'error': 'First name cannot be empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if last_name == '':
                return Response({'error': 'Last name cannot be empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if age == '':
                return Response({'error': 'Age name cannot be empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if date_of_birth == '':
                return Response({'error': 'Date of birth cannot be empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if phone == '':
                return Response({'error': 'Phone cannot be empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if email == '':
                return Response({'error': 'Email cannot be empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if validate_email(email) == False:
                return Response({'error': 'Please enter a valid email '}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except TypeError:
            print("Exception occurred: All the fields are mandotory")
        serilaizer = CreateCustomerAddressSerializer(data=request.data)
        if serilaizer.is_valid(raise_exception=True):
            cursor = connections['default'].cursor()
            try:
                cursor.execute(
                    "SELECT id FROM main_address ORDER BY id DESC LIMIT 1")
                last_insert_id = dictfetchall(cursor)
                if last_insert_id and email and first_name and last_name and age and date_of_birth and phone:
                    cursor.execute("INSERT INTO main_customer(first_name,last_name,age,date_of_birth,phone,email,address_id) VALUES( %s , %s ,%s , %s , %s , %s ,%s)", [
                        first_name, last_name, age, date_of_birth, phone, email, last_insert_id[0]['id']])
                    return Response({'msg': 'Registration Success'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Some fields are empty'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            finally:
                cursor.close()
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)


class cars(APIView):
    def post(self, request, format=None):
        serilaizer = CreateCarSerializer(data=request.data)
        if serilaizer.is_valid(raise_exception=True):
            return Response(serilaizer.data, status=status.HTTP_200_OK)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
