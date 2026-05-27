"""
Custom template filters for the blog app.
"""
import bleach
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# HTML tags that are safe to render in blog post bodies (TinyMCE output)
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 's', 'del',
    'a', 'ul', 'ol', 'li',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote', 'code', 'pre',
    'img', 'figure', 'figcaption',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'hr', 'span', 'div', 'section', 'article',
]

# Attributes allowed per tag
ALLOWED_ATTRIBUTES = {
    '*':        ['class', 'id', 'style'],
    'a':        ['href', 'title', 'target', 'rel'],
    'img':      ['src', 'alt', 'width', 'height', 'loading', 'title'],
    'td':       ['colspan', 'rowspan'],
    'th':       ['colspan', 'rowspan', 'scope'],
    'code':     ['class'],   # syntax highlighting class names
    'pre':      ['class'],
}


@register.filter(name='sanitise_html', is_safe=True)
def sanitise_html(value):
    """
    Sanitise HTML content using bleach before rendering.
    Strips any tags or attributes not in the allow-list and marks it safe.
    Usage: {{ post.body|sanitise_html }}
    """
    if not value:
        return ''
    cleaned = bleach.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,      # Strip disallowed tags (don't escape them)
        strip_comments=True,
    )
    return mark_safe(cleaned)

