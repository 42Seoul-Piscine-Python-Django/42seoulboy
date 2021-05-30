from moviemon.utils.game_data import GameData, save_session_data
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class Title(TemplateView):
    template_name = "title.html"
    context = {}

    def get(self, request):
        key = request.GET.get('key', None)
        if (key is not None):
            print(key)
            if (key == 'a'):
                save_session_data(GameData.load_default_settings().dump())
                return redirect('worldmap')
            elif (key == 'b'):
                return redirect('load_game')
            return redirect(request.path)
        return render(request, self.template_name, self.context)
