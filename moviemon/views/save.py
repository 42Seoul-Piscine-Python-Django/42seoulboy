from moviemon.utils.game_data import load_slot_info, save_slot
from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

optionState = {
    'menu': 0,
}


class Save(TemplateView):
    template_name = "save.html"
    context = {}

    @loadSession_middleware
    def get(self, request):
        key = request.GET.get('key', None)
        if (key is not None):
            print(key)
            if (key == 'up'):
                optionState['menu'] -= 1 if optionState['menu'] > 0 else 0
            elif (key == 'down'):
                optionState['menu'] += 1 if optionState['menu'] < 2 else 0
            if (key == 'a'):
                save_slot(('A', 'B', 'C')[optionState['menu']])
            elif (key == 'b'):
                return redirect('options')
            return redirect(request.path)
        slots = load_slot_info()
        score = 'none' if slots.get(
            'A', None) is None else slots.get('A', 'none').get('score', 'none')
        self.context['A'] = "Slot 🅰 : {}".format(score)
        score = 'none' if slots.get(
            'B', None) is None else slots.get('B', 'none').get('score', 'none')
        self.context['B'] = "Slot 🅱 : {}".format(score)
        score = 'none' if slots.get(
            'C', None) is None else slots.get('C', 'none').get('score', 'none')
        self.context['C'] = "Slot 🅲 : {}".format(score)
        self.context['active'] = optionState['menu']
        return render(request, self.template_name, self.context)
