from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


# Регистрируем наш фильтр под именем bad_words, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter(name='bad_words')
@stringfilter
def bad_words(value):
    """
   value: значение, к которому нужно применить фильтр
   """
    bw_dict = ["редиска", "дурак", "мудак", "сброд"]

    for bw in bw_dict:
        value = value.replace(bw, "*" * len(bw))
        value = value.replace(bw.capitalize(), "*" * len(bw))
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value}'
