from moviemon.utils.game_data import GameData, save_session_data, load_session_data
from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.conf import settings

from .engine.engine import Engine


class Worldmap(TemplateView):
    template_name = "worldmap.html"
    context = {}

    @loadSession_middleware
    def get(self, request):
        game = GameData.load(load_session_data())
        key = request.GET.get('key', None)
        """
        TODO: key에 대한 이벤트 핸들링 필요
        """
        print(game.pos)
        engine = Engine(
            settings.GRID_SIZE,
            settings.SCREEN_SIZE,
            settings.SCREEN_OFFSET,
            game.pos,
            game.movieballCount,
            game.map,
        )
        if (key is not None):
            print(key)
            if (key == 'up'):
                engine.move(0, -1)
            elif (key == 'down'):
                engine.move(0, 1)
            elif (key == 'left'):
                engine.move(-1, 0)
            elif (key == 'right'):
                engine.move(1, 0)
            if (key == 'a'):
                pass
            elif (key == 'b'):
                pass
            elif (key == 'start'):
                return redirect('options')
            elif (key == 'select'):
                return redirect('moviedex')
            game.pos = (engine.px, engine.py)
            game.map = engine.map
            game.movieballCount = engine.movball
            save_session_data(game.dump())
            if engine.state == "battle":
                print("BATTLE")
                return redirect('battle', moviemon_id='tt0468492')
            return redirect(request.path)
        self.context = {
            "engine": engine.render(),
            "movieballs": game.movieballCount,
        }
        return render(request, self.template_name, self.context)
