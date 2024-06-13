from django import template

register = template.Library()

@register.simple_tag
def first3_services(services):
  """
  This tag iterates through the first 3 elements of a queryset.
  """
  return services[:3]
