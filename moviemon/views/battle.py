# from moviemon.middleware.loadSessionMiddleware import loadSession_middleware
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from ..utils.game_data import load_session_data, GameData, save_session_data
import random

battleState= {
    'id': [],
    "text":"Gotcha!! {} "
}




class Battle(TemplateView):
    template_name = "battle.html"
    context = {}

    def get_user_rating(self):
        game = GameData.load(load_session_data())
        captured_list = game.captured_list
        sum_captured_rating = 0
        for i in captured_list :
            # movie_mon = game.moviemon[captured_list[i]]
            sum_captured_rating += game.moviemon[i]['rating']
        if (len(captured_list) == 0):
            return int(sum_captured_rating / 1)
        return int(sum_captured_rating / len(captured_list))
        
    def useball(self, request, moviemon_id):
        game = GameData.load(load_session_data())
            # TODO: 포켓볼 - 1
        getchance = 50 - game.moviemon[moviemon_id]['rating'] * 10 + self.get_user_rating() * 5
        if getchance >= 90 : getchance = 90
        elif getchance <= 1 : getchance = 1
        if getchance > random.randrange(1,101): 
            battleState["text"]= "Gotcha!! {} "
            game.captured_list.append(moviemon_id)
            save_session_data(game.dump())
            print("success")
        return redirect(request.path)


    @loadSession_middleware
    def get(self, request, moviemon_id, key = None):
        game = GameData.load(load_session_data())
        # self.context['moviemon_id'] = moviemon_id
        """
        TODO: moviemon_id를 이용하여 데이터 가져오고 template 한테 전달 필요,
        TODO: key에 대한 이벤트 핸들링 필요
        """
        # game.captured_list = []
        key = request.GET.get('key', None)
        
        if  moviemon_id not in battleState['id']:
            battleState['text'] = "Wild {} appeared."
            battleState['id'].append(moviemon_id)
        if (key is not None):
            print(key)
            if (key == 'a'):
                if moviemon_id in game.captured_list:
                    print("redirect(worldmap)")
                    pass 
                    # return redirect(worldmap)
                else :
                    return self.useball(request, moviemon_id)
            elif (key == 'b'):
                # redirect(self.get(request, moviemon_id, 'b'))
                pass
            elif key == "start":
                pass
            elif key == "select":
                pass
            return redirect(request.path)

        self.context = {
            'moviemon_id': moviemon_id,
            'movie_title': game.moviemon[moviemon_id]['title'],
            'movie_rating': game.moviemon[moviemon_id]['rating'],
            'movie_poster': game.moviemon[moviemon_id]['poster'],
            'user_rating': self.get_user_rating(),
            'user_text': battleState['text'].format(game.moviemon[moviemon_id]['title']) ,
            # 'pocketball_number': game.moviemon['pocketballNumber']
            'pocketball_number': 100
        }
        return render(request, self.template_name, self.context)
