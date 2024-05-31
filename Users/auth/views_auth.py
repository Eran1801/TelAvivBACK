import datetime
import os

import jwt
from Users.auth.decorators import jwt_required
from Users.utilities import encrypt_password, error_response, set_cookie_in_response, success_response, validate_register_data
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from Users.models import Users
from Users.serializers import UsersSerializer
from Users.auth.backends import CustomBackend

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@api_view(['POST'])
@csrf_exempt
def register(request):
    try:
        
        request.data['user_email'] = request.data.get('user_email', '').lower() # set use mail to lower before saving

        # validation checks for user details
        error_message = validate_register_data(request.data)
        if error_message:
            return error_response(message=error_message)

        del request.data['user_password_2']  # no longer needed after validation
        request.data['user_password'] = encrypt_password(request.data.get('user_password'))

        users_serializer = UsersSerializer(data=request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            
            return success_response(message="User created successfully")
        else:
            return error_response(message=users_serializer.errors)

    except Exception as e:
        return error_response(message=f"Error in register function, {e}")


@api_view(['POST'])
@csrf_exempt
def login(request):
    try:
        user_data = request.data

        # extract the right data
        email = user_data.get('user_email').lower()  # lower case email
        password = user_data.get('user_password')

        # authenticate user
        user = CustomBackend.authenticate(username=email, password=password)
        
        if user:
            response = set_cookie_in_response(user)
            return response

        return error_response("email or password incorrect")

    except Exception as e:
        return error_response(message=f"Error in login function, {e}")


@api_view(['DELETE'])
@csrf_exempt
@jwt_required
def delete_user(request):
    try:
        user = Users.objects.get(user_id=request.user_id)

        # delete user, posts, messages from db
        user.delete()

        return success_response(message="Delete successfully")

    except Users.DoesNotExist:
        return error_response("User not found")

    except Exception as e:
        return error_response(message=f"Error deleting user function, {e}")