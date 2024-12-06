import sys
import os
from django.core.wsgi import get_wsgi_application

# Set the project base directory
project_path = '/home/kooroshkz/softdev.kooroshkz.com/UniVerse-AI'
sys.path.insert(0, project_path)

# Set the path to the virtual environment site-packages
venv_path = '/home/kooroshkz/virtualenv/softdev.kooroshkz.com/3.11/lib/python3.11/site-packages'
sys.path.insert(1, venv_path)

# Set the Django settings module environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'UniVerse-AI.settings'

# Activate the virtual environment
activate_env = '/home/kooroshkz/virtualenv/softdev.kooroshkz.com/3.11/bin/activate_this.py'
with open(activate_env) as file_:
    exec(file_.read(), {'__file__': activate_env})

# Create the WSGI application
application = get_wsgi_application()

