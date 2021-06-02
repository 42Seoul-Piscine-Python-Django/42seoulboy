from django.http.response import HttpResponseNotFound
from moviemon.utils.jwt_moviemon import get_moviemonid
from moviemon.utils.game_data import GameData, load_session_data
from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from ..utils.game_data import load_session_data, GameData


position = {"x": 0, "y": 0}


class Moviedex_detail(TemplateView):
    template_name = "moviedex_detail.html"
    context = {}

    @loadSession_middleware
    def get(self, request, moviemon_id):
        game = GameData.load(load_session_data())
        moviemon_id = get_moviemonid(moviemon_id)
        if moviemon_id is None:
            return HttpResponseNotFound(request)
        self.context = {
            "actors": game.get_movie(moviemon_id).actors,
            "director": game.get_movie(moviemon_id).director,
            "plot": game.get_movie(moviemon_id).plot,
            "poster": game.get_movie(moviemon_id).poster,
            "title": game.get_movie(moviemon_id).title,
            "rating": game.get_movie(moviemon_id).rating,
            "year": game.get_movie(moviemon_id).year,
        }
        key = request.GET.get("key", None)
        if key is not None:
            print(key)
            if key == "up":
                position["x"] += 1
            elif key == "down":
                position["x"] -= 1
            elif key == "left":
                position["y"] -= 1
            elif key == "right":
                position["y"] += 1
            if key == "a":
                pass
            elif key == "b":
                return redirect("moviedex")
            elif key == "start":
                pass
            elif key == "select":
                pass
            print(position)
            return redirect(request.path)
        return render(request, self.template_name, self.context)
