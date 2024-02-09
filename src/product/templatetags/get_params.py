from django import template
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