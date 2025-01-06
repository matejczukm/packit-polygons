# import os
# from django.core.management import execute_from_command_line
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
# execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])

import djangoProject
from polygonal_packit.alpha_zero_general.PackitAIPlayer import AIPlayer
if __name__ == '__main__':
    d = {
        'triangular3': AIPlayer(3, 'triangular', local=True, local_folder="C:/Users/piotr/Desktop/inzynierka/packit_polygons/djangoProject/model", local_filename='best_cpuct_5.pth.tar'),
        'triangular5': AIPlayer(5, 'triangular'),
    }
    p = djangoProject.run_app(d)
