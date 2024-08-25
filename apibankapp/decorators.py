# -*- coding: utf-8 -*-

import json
from time import time
from functools import wraps
from .serializers import LogMonitoringSerializer


class ActivityMonitoringClass:

    def __init__(self, show_data=True):
        self.show_data = show_data

    def __call__(self, original_function):

        @wraps(original_function)
        def wrapper(request, *args, **kwargs):
            user_log = str(request.request.user)
            data_log = json.dumps(request.request.data)
            if not self.show_data:
                data_log = 'Data restricted'
            start_time = time()
            action = original_function.__name__
            function = request.__class__.__name__
            result = original_function(request, *args, **kwargs)
            if result.status_code in [200, 201]:
                end_time = time()
                duration = round(end_time - start_time, 6)
                status_log = 'Success'
            else:
                duration = 0
                status_log = 'Failed'
            data = {
                    "action_log": action,
                    "function_log": function,
                    "duration_log": duration,
                    "data_log": data_log[:250],
                    "user_log": user_log,
                    "status_log": status_log}
            serializer = LogMonitoringSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return result    
        return wrapper
