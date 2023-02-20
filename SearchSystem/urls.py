from django.urls import path,include
from .views import *

urlpatterns = [
    # SearchView()视图函数，默认使用的HTML模板路径为templates/search/search.html
    # path(r'search/$', SearchView, name='haystack_search'),
    path('inbase/', inbase),
    path('search_image/', search_image, name="search_image"),
    path('search_text/', search_text, name="search_text"),
    path('search_music/', search_music, name="search_music"),
    path('result/', MySearchView()),
    path('detail/', detail),
]