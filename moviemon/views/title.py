# from moviemon.utils.game_data import GameData, save_session_data
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .engine.keyhandler import Keys
from .engine.engine import Engine

from django.conf import settings

# from moviemon.utils.data import Data

# data = Data()


class Title(TemplateView):
    template_name = "title.html"
    context = {}

    def get(self, request):
        key = Keys("title", request.GET.get("key"))
        print(f"*****{key}*********")
        if len(key):
            if key.get("do") in ["redirect"]:
                # data.load()
                # save_session_data(GameData.load_default_settings().dump())
                return redirect(key.get("args"))
            elif key.get("do") in ["load"]:
                return redirect("load_game")
            return redirect(request.path)
        return render(request, self.template_name, self.context)
