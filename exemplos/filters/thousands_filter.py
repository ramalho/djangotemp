from django.template import Library
from django.template.defaultfilters import floatformat
from django.utils.encoding import force_unicode

register = Library()

@register.filter
def intdot(value):
    orig = force_unicode(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>.\g<2>', orig)
    if orig == new:
        return new
    else:
        return intdot(new)
intdot.is_safe = True

@register.filter
def floatdot(value,precision=-1):
    value = floatformat(value,precision)
    value = force_unicode(value)
    value = value.replace('.',',')
    return intdot(value)
floatdot.is_safe = True

