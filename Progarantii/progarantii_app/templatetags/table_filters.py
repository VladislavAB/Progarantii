from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key1):
    return dictionary.get(key1, {})


@register.filter
def price_range(dictionary, key2):
    return dictionary.get(key2, '')
