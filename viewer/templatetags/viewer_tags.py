from django import template

register = template.Library()

@register.filter
def cut(value, arg):
	"""Removes all values of arg from the given string"""
	return value.replace(arg, '')

@register.filter
def one_static(value):
	"""Removes static from the file name. This avoids {% static %} from generating "/static/static/xxxx" """
	return str(value).replace('static/', '')
	