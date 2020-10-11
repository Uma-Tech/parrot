from html import unescape

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag(takes_context=True, name='absolute')
def get_absolute_url_tag(context, url):
    """Тег возвращающий абсолютный урл."""
    return context.get('request').build_absolute_uri(url)


@register.filter(name='str_to_list')
@stringfilter
def get_headers_list(value, separator):
    """Фильтр создает список из строки."""
    return unescape(value).lstrip('{').rstrip('}').split(separator)
