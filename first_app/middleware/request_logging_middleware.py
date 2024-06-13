from django.utils.deprecation import MiddlewareMixin

from logging import getLogger
from django.utils import timezone
import logging 
import pytz

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware for logging request information, 
    including start time, path, user, method, request data 
    (filtered for POST), and response details.
    """

    def __init__(self, get_response):
       self.get_response = get_response
       self.logger = getLogger(__name__)

    def __call__(self, request):
        """
        Processes the incoming request and logs information before, during, and after request processing.
        """

        start_time = timezone.now()  # Capture start time once


        self.logger.info(
            f'Request started: {request.path} {start_time} {request.user} {request.method}'
            )

        # Handle request data logging based on method
        if request.method == 'GET':
            self.logger.debug(f'Request data(GET): {request.GET}')
        elif request.method == 'POST':
            filtered_post_data = {
            k   : v for k, v in request.POST.items() 
            if k != 'password'
            }
            self.logger.debug(
                f'Request data(POST): {filtered_post_data}'
                )

        response = self.get_response(request)

        # Log information after request processing
        end_time = timezone.now()
        total_time = end_time - start_time

        self.logger.info(
            f'Request completed: {request.method} {request.path} ({ start_time}) (status:{response.status_code})')

        return response




