from django import template

register = template.Library()

@register.filter
def task_color(is_done):
    return 'red' if is_done else 'green'