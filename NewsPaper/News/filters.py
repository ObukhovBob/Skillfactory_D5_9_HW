import django_filters
from django_filters import FilterSet, DateFilter
from django.forms import TextInput
from .models import Post, Author
from django.contrib.auth.models import User


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    date = DateFilter(field_name='timestamp', lookup_expr='lte',  widget=TextInput(attrs={'type': 'date', 'min': '2023-01-01', 'max': '2023-12-31'}))

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            
            # поиск по названию
            'header': ['icontains'],
            'author__user__username': ['icontains'],

        }
