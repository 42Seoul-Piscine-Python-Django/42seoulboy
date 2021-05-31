# from moviemon.utils.game_data import GameData, load_session_data
# from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.conf import settings

from .engine.keyhandler import Keys
from .engine.engine import Engine

position = {"x": 0, "y": 0}


class Worldmap(TemplateView):
    template_name = "worldmap.html"

    # @loadSession_middleware
    def get(self, request):
        const = settings.CONSTANTS
        print(f"CONST IS {const} *******")
        try:
            engine = Engine(
                const["GRID_SIZE"],
                const["SCREEN_SIZE"],
                const["CAMOFFSET"],
                const["PLAYER_INIT_POS"],
            )
        except TypeError:
            print(
                "****** WARNING COULD NOT IMPORT SETTINGS FROM DJANGO.CONF: "
                "RUNNING AS COMPAITABILITY MODE ******"
            )
            engine = Engine((10, 10), (6, 6), (-3, -3))

        key = Keys("worldmap", request.GET.get("key"))
        print("**FROM**", request.GET.get("key"), "**KEY: **", key)
        print("REQUEST.PATH:", request.path)
        self.context = {"engine": engine.render()}
        if key:
            if key.get("do") in ["move"]:
                engine.move(*key.get("args"))
                self.context = {"engine": engine.render()}
                return redirect(request.path)
            elif key.get("do") in ["redirect"]:
                return redirect(key.get("args"))
            elif key.get("do") in ["battle"]:
                pass
            return redirect(request.path)

        return render(request, self.template_name, self.context)
