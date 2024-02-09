from django import template
from django.utils.timesince import timesince
from datetime import datetime
from django.utils import timezone
register = template.Library()


@register.filter(name='get_params')
def get_params(request):
    params = request.GET.copy()
    if params.get("page"):
        params.pop("page")
    param_string =  ""
    for param, value in params.items():
        param_string += "{}={}&".format(param, value)
    return param_string[:-1]



@register.filter
def minutes_ago(value):
    """
    Custom template filter to display the time difference in minutes ago format.
    """
    if isinstance(value, datetime):
        delta = timezone.now() - value
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    return value