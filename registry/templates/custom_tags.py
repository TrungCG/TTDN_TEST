from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight(text, query):
    if not text or not query:
        return text
    pattern = re.escape(query)
    def repl(m):
        return f"<mark>{escape(m.group(0))}</mark>"
    return mark_safe(re.sub(pattern, repl, str(text), flags=re.IGNORECASE))
