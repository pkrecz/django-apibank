# -*- coding: utf-8 -*-

import json
from time import time
from functools import wraps
from .serializers import LogMonitoringSerializer


class ActivityMonitoringClass:

    def __init__(self, decorator_argument):
        self.decorator_argument = decorator_argument
    
    def __call__(self, original_function):

        @wraps(original_function)
        def wrapper(request, *args, **kwargs):
            user = str(request.request.user)
            data = json.dumps(request.request.data)
            start_time = time()
            action = self.decorator_argument
            function = original_function.__name__
            result = original_function(request, *args, **kwargs)
            end_time = time()
            duration = round(end_time - start_time,6)
            status_log = 'Success'
            data = {
                    "action_log": action,
                    "function_log": function,
                    "duration_log": duration,
                    "data_log": data,
                    "user_log": user,
                    "status_log": status_log}
            serializer = LogMonitoringSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return result    
        return wrapper
