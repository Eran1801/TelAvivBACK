from django.db import connection
from django.http.response import JsonResponse
from django.views.decorators.csrf import \
    csrf_exempt  # will be used to exempt the CSRF token (Angular will handle CSRF token)
from rest_framework.parsers import JSONParser
from django.http import *
from rest_framework.decorators import api_view
from Users.models import Users
from Users.serializers import UsersSerializer
import re
import hashlib
import logging
from validate_email import validate_email

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def check_valid_password(pas:str) -> bool:
    '''check if the password is valid'''
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)' # contains at least one upper and one lower letter and number.
    return True if re.match(pattern,pas) and len(pas) >= 8 else False # adding the big&equal from 8

def hash_password(plain_password:str) -> str:
    '''encrypt the password user using sha256 algorithm'''
    sha256 = hashlib.sha256()
    sha256.update(plain_password.encode('utf-8'))
    hashed_password = sha256.hexdigest()

    return hashed_password

def email_exists(email:str) -> bool:
    '''exists() method returns True if user_email already in the db'''
    return Users.objects.filter(user_email=email).exists()

def phone_exists(phone:str)-> bool:
    '''returns True if at least one record matches the filter, and False if no records match.'''
    return Users.objects.filter(user_phone=phone).exists()

def full_name_check(full_name:str) -> bool:
    '''
    check if the full name is valid
    full name must be at least 4 characters and contain at least one space.
    '''
    return True if len(full_name) >= 4 and full_name.count(' ') > 0 else False

def phone_number_check(phone_number:str) -> bool:
    '''
    check if the phone number is valid.
    phone number must be at least 10 characters.    
    '''
    return True if len(phone_number) >= 10 else False

@api_view(['POST'])
@csrf_exempt
def register(request, user_id = 0): 
    '''
    This function will be used to add a new user.
    user_id = 0, start user_id from 0 and increment by 1 each time a new user is added.
    MORE FROM THE FUNCTION:
    1. check if the email and phone number already exist in the db.
    2. check if the full name, phone number, and password are valid.
    3. encrypt the password before saving it to the db.
    4. save the user to the db.
    '''

    user_data = JSONParser().parse(request) # access individual fields, users_data.get('field_name')
    
    user_full_name = user_data.get('user_full_name')
    user_email = user_data.get('user_email').lower() # lower case email
    user_phone_number = user_data.get('user_phone')
    user_password = user_data.get('user_password')
    user_password_2 = user_data.get('user_password_2')
    
    # checks valid register input from user
    check_full_name: bool = full_name_check(user_full_name)
    check_email = validate_email(user_email)
    check_phone_number = phone_number_check(user_phone_number)
    check_password = check_valid_password(user_password)

    if user_password == user_password_2: # checking if 2 user passwords are equal

        user_data['user_password'] = hash_password(user_password) # encrypt before saving

        if email_exists(user_email): 
            return HttpResponseServerError('Email already exists')
        
        if phone_exists(user_phone_number):
            return HttpResponseServerError('Phone number already exists')
        
        if not check_full_name:
            return HttpResponseServerError('Invalid full name')
        
        if not check_phone_number:
            return HttpResponseServerError('Invalid phone number')
        
        if not check_password:
            return HttpResponseServerError('Invalid password')
        
        if not check_email:
            return HttpResponseServerError('Invalid email')

        del user_data['user_password_2'] # don't needs to be save in the db
        
        users_serializer = UsersSerializer(data=user_data)
        if users_serializer.is_valid():
            users_serializer.save() # save to db
            return JsonResponse("Register Success",safe=False)
        else:
            logger.debug(users_serializer.errors)
            return HttpResponseServerError("Register Fails")
    else:
        return HttpResponseServerError("Passwords don't match.")
        
@api_view(['POST'])
@csrf_exempt
def login(request):
    '''
    This function will be used to login a user.
    1. check if the email exists in the db.
    2. encrypt the password before comparing it to the password in the db.
    3. check if the passwords match.
    '''
    user_data = JSONParser().parse(request)

    login_email_address = user_data.get('user_email').lower() # lower case email 
    login_password = user_data.get('user_password')

    # encrypt user password for check similarity in the db
    hash_password_login = hash_password(login_password) 
    
    try:
        user = Users.objects.get(user_email=login_email_address) # retrieve user from db based on email

        if user.user_password == hash_password_login:

            response_data = {
            'user': {
                'user_id': user.user_id,
                'user_full_name': user.user_full_name,
                'user_email': user.user_email,
                'user_phone': user.user_phone
            },
                'message': 'Passwords match. Login successfully'
            }
            
            return JsonResponse(response_data)
        else:
            return HttpResponseServerError("Passwords don't match. Login fail")
    except Users.DoesNotExist:
        return HttpResponseServerError("User not found.")
    
    