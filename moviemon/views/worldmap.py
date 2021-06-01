from moviemon.utils.jwt_moviemon import get_moviemon_token
from moviemon.utils.game_data import GameData, save_session_data, load_session_data
from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.conf import settings

from .engine.engine import Engine

worldmap_flush = {'flush': False}


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
        # print(game.moviemon)
        # print(game.get_random_movie())
        engine = Engine(
            settings.GRID_SIZE,
            settings.SCREEN_SIZE,
            settings.SCREEN_OFFSET,
            game.pos,
            game.movieballCount,
            game.map,
        )
        if (key is not None):
            # print(key)
            if (key == 'up'):
                if worldmap_flush['flush'] is False:
                    engine.move(0, -1)
            elif (key == 'down'):
                if worldmap_flush['flush'] is False:
                    engine.move(0, 1)
            elif (key == 'left'):
                if worldmap_flush['flush'] is False:
                    engine.move(-1, 0)
            elif (key == 'right'):
                if worldmap_flush['flush'] is False:
                    engine.move(1, 0)
            if (key == 'a'):
                if worldmap_flush['flush'] is True:
                    worldmap_flush['flush'] = False
                    return redirect('battle', moviemon_id=get_moviemon_token(game.get_random_movie()))
                pass
            elif (key == 'b'):
                pass
            elif (key == 'start'):
                if worldmap_flush['flush'] is False:
                    return redirect('options')
            elif (key == 'select'):
                if worldmap_flush['flush'] is False:
                    return redirect('moviedex')
            game.pos = (engine.px, engine.py)
            game.map = engine.map
            game.movieballCount = engine.movball
            print("saving...")
            save_session_data(game.dump())
            if engine.state == "battle":
                print("BATTLE")
                worldmap_flush['flush'] = True
                # return redirect('battle', moviemon_id=game.get_random_movie())
            return redirect(request.path)
            # return redirect('battle', moviemon_id=game.get_random_movie())
        self.context = {
            "flush": worldmap_flush['flush'],
            "engine": engine.render(),
            "movieballs": game.movieballCount,
        }
        return render(request, self.template_name, self.context)
