# import os
# from django.core.management import execute_from_command_line
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
# execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])

import djangoProject
if __name__ == '__main__':
    d = {
        'eee': 'eff',
        'defe': 'sss'
    }
    p = djangoProject.run_app(d, verbose=1)
    print(p)
