import os
import subprocess
import webbrowser
from django.core.management.utils import get_random_secret_key
import time
# import sys
# sys.path.append('..')
# from packitPolygons.ai_players_registry import AIPlayerRegistry
from django.core.cache import cache

import win32api
import win32con
import win32job


def run_app(ai_players_dict, port=8000, verbose=False):
    # for name, player in ai_players_dict.items():
    #     AIPlayerRegistry.add_player(name, player)
    # # print(AIPlayerRegistry.get_players())
    # print("Before adding players:", AIPlayerRegistry.get_players())
    # AIPlayerRegistry.add_player("kkk", "ssrw")
    # print("After adding players:", AIPlayerRegistry.get_players())

    hJob = win32job.CreateJobObject(None, "")
    extended_info = win32job.QueryInformationJobObject(hJob, win32job.JobObjectExtendedLimitInformation)
    extended_info['BasicLimitInformation']['LimitFlags'] = win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    win32job.SetInformationJobObject(hJob, win32job.JobObjectExtendedLimitInformation, extended_info)

    # Set environment variables for Django settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")

    # Generate a random secret key if not set
    secret_key = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())
    os.environ["DJANGO_SECRET_KEY"] = secret_key

    # Start the server process
    process = subprocess.Popen(
        ["python", "manage.py", "runserver", f"127.0.0.1:{port}"],
        shell=True,
        stdout=None if verbose else subprocess.PIPE,
        stderr=None if verbose else subprocess.PIPE,
        # start_new_session=True  # Prevent the child process from being killed by Ctrl+C
    )
    perms = win32con.PROCESS_TERMINATE | win32con.PROCESS_SET_QUOTA
    hProcess = win32api.OpenProcess(perms, False, process.pid)
    cache.set("ai_players", {"xx": "esaesa", "xfdq": "ddsa"})
    players = cache.get("ai_players", {})
    print("Players in run_app:", players)
    win32job.AssignProcessToJobObject(hJob, hProcess)
    time.sleep(2)
    # webbrowser.open(f"http://127.0.0.1:{port}")

    try:
        input("Press Enter to stop the server...")
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == '__main__':
    d = {
        'sss': 'seffc',
        'scwdff': 'sss'
    }
    run_app(d)
