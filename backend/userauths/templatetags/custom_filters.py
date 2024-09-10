from django import template

register = template.Library()


@register.filter
def length_is(value, arg):
   """
   Filter that checks if the length of a value is equal to the provided argument.
   """
   return len(value) == arg
