from moviemon.utils.jwt_moviemon import get_moviemon_token
from moviemon.utils.game_data import (
    GameData,
    save_session_data,
    load_session_data,
)
from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.conf import settings

from .engine.engine import Engine
from .engine.message import Message

states = {"flush": None}
msg = Message("none")
worldstate = None


class Worldmap(TemplateView):
    template_name = "worldmap.html"
    context = {}

    def checkwin(self, game):
        if len(game.captured_list) >= len(game.moviemon):
            print("WINGAME")
            states["flush"] = "win"
        elif states["flush"] == "win":
            states["flush"] = None

    @loadSession_middleware
    def get(self, request):
        game = GameData.load(load_session_data())
        key = request.GET.get("key", None)
        # print(game.pos)
        gotmovie = f"{len(game.captured_list)}/{len(game.moviemon)}"
        print(gotmovie)
        self.checkwin(game)
        # print(game.get_random_movie())
        engine = Engine(
            settings.GRID_SIZE,
            settings.SCREEN_SIZE,
            settings.SCREEN_OFFSET,
            game.pos,
            game.movieballCount,
            len(game.moviemon),
            len(game.captured_list),
            game.map,
        )
        if not states["flush"] and msg.key == "battle":
            msg("none", single=True)
        if key and not states["flush"] == "win":
            # print(key)
            if not states["flush"]:
                if key == "up":
                    engine.move(0, -1)
                elif key == "down":
                    engine.move(0, 1)
                elif key == "left":
                    engine.move(-1, 0)
                elif key == "right":
                    engine.move(1, 0)
                elif key == "start":
                    return redirect("options")
                elif key == "select":
                    return redirect("moviedex")
            else:
                if key == "a":
                    if states["flush"] == "battle":
                        states["flush"] = None
                        return redirect(
                            "battle",
                            moviemon_id=get_moviemon_token(
                                game.get_random_movie()
                            ),
                        )
                    else:
                        raise Exception("invalid state", states["flush"])
                pass
            if key == "b":
                pass

            game.pos = (engine.px, engine.py)
            game.map = engine.map
            game.movieballCount = engine.movball
            print("saving...")
            save_session_data(game.dump())

            if engine.state == "battle":
                print("BATTLE")
                states["flush"] = "battle"
                msg(engine.state, single=True)
                # return redirect('battle', moviemon_id=game.get_random_movie())
            elif engine.state:
                msg(engine.state)
            return redirect(request.path)
            # return redirect('battle', moviemon_id=game.get_random_movie())
        elif key and key == "a" and states["flush"] == "win":
            return redirect("title")
        self.context = {
            "flush": states["flush"],
            "engine": engine.render(),
            "movieballs": game.movieballCount,
            "message": str(msg),
            "moviemons": len(game.moviemon),
        }
        return render(request, self.template_name, self.context)
