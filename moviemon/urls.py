from moviemon.views.option import Option, OptionLoad, OptionSave
from django.urls import path
from .views import Title, Battle, Worldmap, Moviedex, Moviedex_detail

urlpatterns = [
    path('', Title.as_view(), name='Title'),
    path('worldmap', Worldmap.as_view(), name='worldmap'),
    path('battle/<str:moviemon_id>', Battle.as_view(), name='battle'),
    path('moviedex', Moviedex.as_view(), name='moviedex'),
    path('moviedex/<str:moviemon_id>',
         Moviedex_detail.as_view(), name='moviedex_detail'),
    path('options', Option.as_view(), name='options'),
    path('options/save_game', OptionSave.as_view(), name='save_game'),
    path('options/load_game', OptionLoad.as_view(), name='load_game'),
]
