# from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

# from ..utils.game_data import load_session_data, GameData

MoviedexState = {"posistion": 0}


class Moviedex(TemplateView):
    template_name = "moviedex.html"
    context = {}

    # @loadSession_middleware
    def get(self, request):
        # game = GameData.load(load_session_data())
        game = None
        key = request.GET.get("key", None)
        if key is not None:
            print(key)
            if key == "up":
                pass
            elif key == "down":
                pass
            elif key == "left":
                if MoviedexState["posistion"] > 0:
                    MoviedexState["posistion"] -= 1
            elif key == "right":
                if MoviedexState["posistion"] < len(game.captured_list) - 1:
                    MoviedexState["posistion"] += 1
            if key == "a":
                pass
            elif key == "b":
                return redirect("worldmap")
            elif key == "start":
                pass
            elif key == "select":
                pass
            return redirect(request.path)

        self.context["movies"] = []

        if MoviedexState["posistion"] > 0:
            id = game.captured_list[MoviedexState["posistion"] - 1]
            self.context["movies"].append(
                {
                    "poster": game.moviemon[id]["poster"],
                    "class": "moviedex-blur",
                }
            )
        if len(game.captured_list) > 0:
            id = game.captured_list[MoviedexState["posistion"]]
            self.context["movies"].append(
                {
                    "poster": game.moviemon[id]["poster"],
                    "class": "moviedex-ative ",
                }
            )
        if MoviedexState["posistion"] < len(game.captured_list) - 1:
            id = game.captured_list[MoviedexState["posistion"] + 1]
            self.context["movies"].append(
                {
                    "poster": game.moviemon[id]["poster"],
                    "class": "moviedex-blur",
                }
            )
        if MoviedexState["posistion"] == 0 and 1 < len(game.captured_list):
            id = game.captured_list[2]
            self.context["movies"].append(
                {
                    "poster": game.moviemon[id]["poster"],
                    "class": "moviedex-blur",
                }
            )

        return render(request, self.template_name, self.context)
