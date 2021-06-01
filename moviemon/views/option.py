from moviemon.utils.game_data import load_slot_info
from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class Option(TemplateView):
    template_name = "option.html"
    context = {}

    def get(self, request):
        key = request.GET.get('key', None)
        if (key is not None):
            if (key == 'a'):
                return redirect('save_game')
            elif (key == 'b'):
                return redirect('title')
            elif (key == 'start'):
                return redirect('worldmap')
            return redirect(request.path)
        return render(request, self.template_name, self.context)
