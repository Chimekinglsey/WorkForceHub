# This middleware is used to handle exceptions and render a custom 500 error page
from django.http import Http404
from logging import getLogger, FileHandler, Formatter
from django.shortcuts import render


# Initialize logger
logger = getLogger(__name__)
logger_404 = getLogger('error_404')

logger_404.setLevel(30)
logger.setLevel(30) 

# Log file path where logs will be stored
log_500_file = 'error_files/error_500.txt'
log_404_file = 'error_files/error_404.txt'

# File handler
file_handler = FileHandler(log_500_file)
file_handler_404 = FileHandler(log_404_file)

# Set log level for file handler
file_handler.setLevel(30)  
file_handler_404.setLevel(30)

# Log message format
log_format = '%(asctime)s - %(client_ip)s - %(requested_resource)s - %(message)s'
formatter = Formatter(log_format)

# Set formatter for file handler
file_handler.setFormatter(formatter)
file_handler_404.setFormatter(formatter)

# Add file handler to logger
logger.addHandler(file_handler)
logger_404.addHandler(file_handler_404)


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Log exception to file
        logger.error(exception, extra={
            'client_ip': request.META.get('REMOTE_ADDR'),
            'requested_resource': f"requested_resource: {request.path}",
        })

        # Render custom 500 error page
        context = {'exception': exception}
        return render(request, 'error/500.html', status=500, context=context)

class NotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            # # Log 404 error to file
            # logger_404.error(exception, extra={
            #     'client_ip': request.META.get('REMOTE_ADDR'),
            #     'requested_resource': f"requested_resource: {request.path}",
            # })
            return render(request, '404.html', status=404)
        return None
    
class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return self.handle_404(request)
        return response

    def handle_404(self, request, exception=None):
        # Render your custom 404 template
        return render(request, '404.html', status=404)