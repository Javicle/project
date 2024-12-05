from django import template

register = template.Library()


@register.filter
def is_long_title(article_title: str) -> bool:
    if article_title is None:
        article_title = ""
    return len(article_title) >= 8
