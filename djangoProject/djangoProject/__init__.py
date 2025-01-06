import os
import webbrowser
from django.core.management import call_command
from django.core.management.utils import get_random_secret_key
import time
import django
from packitPolygons.ai_players_registry import AIPlayerRegistry


def run_app(ai_players_dict, open_browser=True):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")

    secret_key = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())
    os.environ["DJANGO_SECRET_KEY"] = secret_key

    django.setup()
    for name, player in ai_players_dict.items():
        AIPlayerRegistry.add_player(name, player)

    if open_browser:
        webbrowser.open("http://127.0.0.1:8000")

    try:
        call_command("runserver", "127.0.0.1:8000", use_reloader=False)
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    d = {
        "siema": "eniu",
        "elo": "sss"
    }
    run_app(d)
