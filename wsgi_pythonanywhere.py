#!/usr/bin/env python3.10

import os
import sys

# Add your project directory to sys.path
path = '/home/yourusername/FashionFit'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'FashionFit.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
