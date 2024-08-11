import json
from time import time
from functools import wraps
from .models import LogModel
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response


class ActivityMonitoringClass:

    def __init__(self, decorator_argument):
        self.decorator_argument = decorator_argument
    
    def __call__(self, original_function):

        @wraps(original_function)
        def wrapper(request, *args, **kwargs):
            try:
                with transaction.atomic():
                    user = request.request.user
                    data = json.dumps(request.request.data)
                    start_time = time()
                    action = self.decorator_argument
                    function = original_function.__name__
                    result = original_function(request, *args, **kwargs)
                    end_time = time()
                    duration = round(end_time - start_time,6)
                    LogModel.objects.create(action_log=action, function_log=function, duration_log=duration, data_log=data, user_log=user, status_log='Success')
                    return result
            except:
                LogModel.objects.create(action_log=action, function_log=function, duration_log=0, data_log=data, user_log=user, status_log='Failed')
                return Response({'message': 'Atomic transaction was not executed!'}, status=status.HTTP_400_BAD_REQUEST)
        return wrapper
