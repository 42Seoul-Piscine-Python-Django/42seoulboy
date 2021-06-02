from moviemon.utils.jwt_moviemon import get_moviemonid
from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http.response import HttpResponseNotFound
from ..utils.game_data import load_session_data, GameData, save_session_data
from .engine.utils import clip
import random

battleState = {
    "id": "",
    "text": "Gotcha!! {} ",
    "button-text": "🅰 Launch Movie Ball   🅱 Run",
}


class Battle(TemplateView):
    template_name = "battle.html"
    context = {}

    # def get_user_rating(self):
    #     game = GameData.load(load_session_data())
    #     captured_list = game.captured_list
    #     sum_captured_rating = 0
    #     for i in captured_list:
    #         # movie_mon = game.moviemon[captured_list[i]]
    #         sum_captured_rating += game.moviemon[i].rating
    #     if (len(captured_list) == 0):
    #         return int(sum_captured_rating / 1)
    #     return int(sum_captured_rating / len(captured_list))
    def calculate_winning_rate(self, game, moviemon_id):
        # TODO: 포켓볼 - 1
        getchance = (
            50
            - game.moviemon[moviemon_id].rating * 10
            + game.get_strength() * 5
        )
        # return 100
        return clip(getchance, (1, 90))

    def useball(self, game, request, moviemon_id):
        getchance = self.calculate_winning_rate(game, moviemon_id)
        if getchance >= random.randrange(1, 101):
            battleState["text"] = "Gotcha!! {} "
            battleState["button-text"] = "🅰 Continue"
            game.captured_list.append(moviemon_id)
            save_session_data(game.dump())
            print("success")
        else:
            battleState["text"] = "You missed !"
            print("fail")
        return redirect(request.path)

    @loadSession_middleware
    def get(self, request, moviemon_id, key=None):
        game = GameData.load(load_session_data())
        moviemon_id = get_moviemonid(moviemon_id)
        if moviemon_id is None or game.moviemon.get(moviemon_id, None) is None:
            return HttpResponseNotFound(request)
        # self.context['moviemon_id'] = moviemon_id
        """
        TODO: moviemon_id를 이용하여 데이터 가져오고 template 한테 전달 필요,
        TODO: key에 대한 이벤트 핸들링 필요
        """
        # game.captured_list = []
        key = request.GET.get("key", None)

        # if moviemon_id not in battleState['id']:
        if moviemon_id not in game.captured_list:
            if moviemon_id != battleState["id"]:
                battleState["text"] = "Wild {} appeared."
                battleState["button-text"] = "🅰 Launch Movie Ball   🅱 Run"
                battleState["id"] = moviemon_id
        else:
            battleState["text"] = "Gotcha!! {} "
            battleState["button-text"] = "🅱 Continue"

        if key is not None:
            print(key)
            if key == "a":
                if moviemon_id not in game.captured_list:
                    if game.movieballCount < 1:
                        return redirect(request.path)
                    game.movieballCount -= 1
                    save_session_data(game.dump())
                    return self.useball(game, request, moviemon_id)
            elif key == "b":
                battleState["text"] = "Wild {} appeared."
                return redirect("worldmap")
            elif key == "start":
                pass
            elif key == "select":
                pass
            return redirect(request.path)
        self.context = {
            "moviemon_id": moviemon_id,
            "movie_title": game.moviemon[moviemon_id].title,
            "movie_poster": game.moviemon[moviemon_id].poster,
            "movie_rating": game.moviemon[moviemon_id].rating,
            "user_rating": game.get_strength(),
            "user_text": battleState["text"].format(
                game.moviemon[moviemon_id].title
            ),
            "pocketball_number": game.movieballCount,
            "button_text": battleState["button-text"],
            "user_winning_rate": "⚔️ {}%".format(
                str(self.calculate_winning_rate(game, moviemon_id))
            ),
        }
        return render(request, self.template_name, self.context)
