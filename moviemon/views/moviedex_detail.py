from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from ..utils.game_data import load_session_data, GameData


position = {
    'x': 0,
    'y': 0
}


class Moviedex_detail(TemplateView):
    template_name = "moviedex_detail.html"
    context = {}

    @loadSession_middleware
    def get(self, request, moviemon_id):
        game = GameData.load(load_session_data())
        self.context = game.moviemon[moviemon_id]
        key = request.GET.get('key', None)
        if (key is not None):
            print(key)
            if (key == 'up'):
                position['x'] += 1
            elif (key == 'down'):
                position['x'] -= 1
            elif (key == 'left'):
                position['y'] -= 1
            elif (key == 'right'):
                position['y'] += 1
            if (key == 'a'):
                pass
            elif (key == 'b'):
                return redirect('moviedex')
            elif (key == 'start'):
                pass
            elif (key == 'select'):
                pass
            print(position)
            return redirect(request.path)
        return render(request, self.template_name, self.context)
