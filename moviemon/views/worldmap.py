# from moviemon.utils.game_data import GameData, load_session_data
# from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.conf import settings

from .engine.keyhandler import Keys
from .engine.engine import Engine

from moviemon.utils.data import Data

data = Data()
const = settings.CONSTANTS


class Worldmap(TemplateView):
    try:
        engine = Engine(
            const["GRID_SIZE"],
            const["SCREEN_SIZE"],
            const["CAMOFFSET"],
            data.get("pos"),
        )
        print("HELLO")

    except Exception:
        print(
            "****** WARNING COULD NOT IMPORT SETTINGS FROM DJANGO.CONF: "
            "RUNNING AS COMPAITABILITY MODE ******"
        )
        engine = Engine(
            const["GRID_SIZE"], const["SCREEN_SIZE"], const["CAMOFFSET"], (5, 5)
        )

    template_name = "worldmap.html"
    # print(data.dump())
    # @loadSession_middleware
    def get(self, request):
        data.load()
        # print(f"CONST IS {const} *******")
        key = Keys("worldmap", request.GET.get("key"))
        # print("**FROM**", request.GET.get("key"), "**KEY: **", key)
        # for k, v in data.dump().items():
        #     if k not in ["map", "not_yet_moviemons"]:
        #         print(f"key:{k}, value:{v}")
        # print("REQUEST.PATH:", request.path)
        self.context = {"engine": self.engine.render()}
        if key:
            if key.get("do") in ["move"]:
                self.engine.move(*key.get("args"))
                self.context = {"engine": self.engine.render()}
                data.update("pos", (self.engine.px, self.engine.py))
                data.update("map", self.engine.map, save=True)
                return redirect(request.path)
            elif key.get("do") in ["redirect"]:
                return redirect(key.get("args"))
            elif key.get("do") in ["battle"]:
                pass
            return redirect(request.path)

        return render(request, self.template_name, self.context)
