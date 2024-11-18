from django import template
from crispy_forms.utils import render_crispy_form

from ..forms import AuthenticationForm

register = template.Library()


@register.simple_tag(takes_context=True)
def login_form(context):
    form = AuthenticationForm()
    return render_crispy_form(form, None, context)
