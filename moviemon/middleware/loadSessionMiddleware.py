from django.shortcuts import redirect
from functools import wraps
from ..utils.game_data import GameData, load_session_data


def loadSession_middleware(view_function):
    @wraps(view_function)
    def wrap(request, *args, **kwargs):
        data = load_session_data()
        if data is None:
            return redirect("title")
        return view_function(request, *args, **kwargs)
    return wrap
