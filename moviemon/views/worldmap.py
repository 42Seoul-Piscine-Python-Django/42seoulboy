from moviemon.utils.game_data import GameData, load_session_data
from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


position = {
    'x': 0,
    'y': 0
}


class Worldmap(TemplateView):
    template_name = "worldmap.html"
    context = {}

    @loadSession_middleware
    def get(self, request):
        key = request.GET.get('key', None)
        """
        TODO: key에 대한 이벤트 핸들링 필요
        """
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
                pass
            elif (key == 'start'):
                return redirect('options')
            elif (key == 'select'):
                return redirect('moviedex')
            print(position)
            return redirect(request.path)
        return render(request, self.template_name, self.context)
