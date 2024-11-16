# -*- coding: utf-8 -*-

import json
from .serializers import LogMonitoringSerializer


class RegisterErrorClass:

    def register_error(self, request):
        user_log = str(request.user)
        data_log = json.dumps(request.data)
        action = self.action
        function = self.__class__.__name__
        status_log = "Failed"
        data = {
                "action_log": action,
                "function_log": function,
                "duration_log": 0,
                "data_log": data_log[:250],
                "user_log": user_log,
                "status_log": status_log}
        serializer = LogMonitoringSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
