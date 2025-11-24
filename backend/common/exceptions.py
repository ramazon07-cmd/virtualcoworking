from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Log the exception
    logger.error(f"Exception occurred: {exc}", exc_info=True)
    
    # Customize the response
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': response.data.get('detail', 'An error occurred'),
            'status_code': response.status_code,
        }
        
        # Handle validation errors
        if isinstance(response.data, dict) and 'detail' not in response.data:
            custom_response_data['errors'] = response.data
        
        response.data = custom_response_data
    
    return response