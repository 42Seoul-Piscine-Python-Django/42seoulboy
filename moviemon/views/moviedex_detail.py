from django.shortcuts import redirect, render
from django.views.generic import TemplateView


position = {
    'x': 0,
    'y': 0
}


class Moviedex_detail(TemplateView):
    template_name = "moviedex_detail.html"
    context = {}

    def get(self, request, moviemon_id):
        self.context['moviemon_id'] = moviemon_id
        """
        TODO: moviemon_id를 이용하여 데이터 가져오고 template 한테 전달 필요,
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
