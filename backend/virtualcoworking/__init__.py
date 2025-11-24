import os
import sys

# Add the config directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

from celery import app as celery_app

__all__ = ('celery_app',)