"""
WSGI config for prisencolin_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/opt/bitnami/projects/fantasy-language-speech-generator')

os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/projects/fantasy-language-speech-generator/egg_cache")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prisencolin_project.settings')

application = get_wsgi_application()
