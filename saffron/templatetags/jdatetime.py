import jdatetime
from django import template
register = template.Library()


@register.filter(name='jdate')
def jdate(georgian_datetime):
    timestamp = georgian_datetime.timestamp()
    jalalian_datetime = jdatetime.datetime.fromtimestamp(timestamp)
    return jalalian_datetime.strftime("%Y/%m/%d")


