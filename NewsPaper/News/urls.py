from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, Article, NewsSearch, ArticleCreate, NewsCreate, NewsUpdate, ArticleList


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем новостям у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('NW', NewsList.as_view()),
   path('AR', ArticleList.as_view()),
   # pk — это первичный ключ новости, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', Article.as_view(), name='article'),
   path('search/', NewsSearch.as_view(), name='search'),
   path('NW/create', NewsCreate.as_view(), name='news_create'),
   path('AR/create', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update')

]