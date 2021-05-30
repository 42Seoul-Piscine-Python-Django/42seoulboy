from django.shortcuts import redirect, render
from django.views.generic import TemplateView


position = {
    'x': 0,
    'y': 0
}


class Option(TemplateView):
    template_name = "option.html"
    context = {}

    def get(self, request):
        """
        TODO: key에 대한 이벤트 핸들링 필요
        """
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
                pass
            elif (key == 'start'):
                pass
            elif (key == 'select'):
                pass
            print(position)
            return redirect(request.path)
        return render(request, self.template_name, self.context)


class OptionSave(TemplateView):
    template_name = "save.html"
    context = {}

    def get(self, request):
        """
        TODO: key에 대한 이벤트 핸들링 필요
        """
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
                pass
            elif (key == 'start'):
                pass
            elif (key == 'select'):
                pass
            print(position)
            return redirect(request.path)
        return render(request, self.template_name, self.context)


class OptionLoad(TemplateView):
    template_name = "load.html"
    context = {}

    def get(self, request):
        """
        TODO: key에 대한 이벤트 핸들링 필요
        """
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
                pass
            elif (key == 'start'):
                pass
            elif (key == 'select'):
                pass
            print(position)
            return redirect(request.path)
        return render(request, self.template_name, self.context)
