# from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.base import View

from moviemon.utils.data import Data

# from ..utils.game_data import load_session_data, GameData


MoviedexState = {"posistion": 0}

data = Data()


class Moviedex(TemplateView):
    template_name = "moviedex.html"
    context = {}

    # @loadSession_middleware
    def get(self, request):
        def now(setval=None, abso=False):
            """
            now() 를 입력하면... MoviedexState["posistion"]를 반환한다\n
            now(값) 을 입력하면... MoviedexState["posistion"]에 값만큼 변동\n
            now(값, True) 를 입력하면... MoviedexState["posistion"]에 값 대입
            """
            if setval and abso:
                MoviedexState["posistion"] = setval
            elif setval:
                MoviedexState["posistion"] += setval
            else:
                return MoviedexState["posistion"]

        # game = GameData.load(load_session_data())
        mymons = data.get("my_moviemons")
        mylst = [[k, v] for k, v in mymons.items()]

        print("mymons:")
        # for k, v in mymons.items():
        #     print(v.data)
        # ["영화 id", "무비몬 인스턴스"] 로 구성된 리스트

        if now() >= len(mylst):
            now(0, True)
        key = request.GET.get("key", None)
        if key is not None:
            print(key)
            if key == "up":
                pass
            elif key == "down":
                pass
            elif key == "left":
                if now() > 0:
                    now(-1)
            elif key == "right":
                if now() < len(mylst) - 1:
                    now(1)
            if key == "a":
                return redirect(
                    "moviedex_detail",
                    moviemon_id=mylst[now()][0],
                )
            elif key == "b":
                return redirect("worldmap")
            elif key == "start":
                pass
            elif key == "select":
                pass
            return redirect(request.path)

        self.context["movies"] = []
        if now() > 0:
            mov_id = mylst[now() - 1][0]
            print("mov_id:", mov_id)
            self.context["movies"].append(
                {
                    "poster": data.get_movie(mov_id)["poster"],
                    "class": "moviedex-blur",
                }
            )
        if len(mylst) > 0:
            mov_id = mylst[now()][0]
            print("mov_id:", mov_id)
            self.context["movies"].append(
                {
                    "poster": data.get_movie(mov_id)["poster"],
                    "class": "moviedex-ative ",
                }
            )
        if now() < len(mylst) - 1:
            mov_id = mylst[now() + 1][0]
            print("mov_id:", mov_id)
            self.context["movies"].append(
                {
                    "poster": data.get_movie(mov_id)["poster"],
                    "class": "moviedex-blur",
                }
            )
        if now() == 0 and 1 < len(mylst):
            mov_id = mylst[2][0]
            print("mov_id:", mov_id)
            self.context["movies"].append(
                {
                    "poster": data.get_movie(mov_id)["poster"],
                    "class": "moviedex-blur",
                }
            )

        return render(request, self.template_name, self.context)
