from django import template
from django.templatetags.static import static
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe, SafeString

from ..emoticons import emoticons


register = template.Library()


@register.simple_tag
@register.filter(name="emoticons")
def apply_emoticons(text):
    if not isinstance(text, SafeString):
        text = conditional_escape(text)

    for emoticon, image_url in emoticons:
        text = text.replace(
            emoticon,
            f'<img class="inline image-pixelated" src="{static(image_url)}" alt="{emoticon}" />',
        )

    return mark_safe(text)
