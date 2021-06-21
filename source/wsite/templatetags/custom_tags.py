from django import template

register = template.Library()


def underscorefix(obj, attribute):
  return getattr(obj, attribute)
    
register.filter('usfix', underscorefix)