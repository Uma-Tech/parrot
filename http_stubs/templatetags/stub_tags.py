from html import unescape
from typing import AnyStr, Dict, List

from django import template
from django.template.defaultfilters import stringfilter

Url = str

register = template.Library()


@register.simple_tag(takes_context=True, name='absolute')
def get_absolute_url_tag(context: Dict, url: Url) -> Url:
    """Tag that returns an absolute url.

    :param context: context of request
    :param url: relative url
    :returns: absolute url
    """
    return context.get('request').build_absolute_uri(url)


@register.filter(name='headers_to_list')
@stringfilter
def get_headers_list(headers: AnyStr, separator: AnyStr) -> List:
    """Filter that creates a list from a string of headers(dict).

    :param headers: string of headers
    :param separator: separator to separate string
    :returns: list of headers
    """
    return unescape(headers).lstrip('{').rstrip('}').split(separator)
