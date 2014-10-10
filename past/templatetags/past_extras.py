from django import template
from django.utils.safestring import mark_safe

import re

register = template.Library()


@register.filter(name='addReferences')
def addReferences(text):
    """Turns all instances of [1] into the link to that reference"""
    regexMatch = re.compile(r'(\[\d+\])')
    print text
    for match in regexMatch.findall(text):
        print match
        id = match.replace("[", "").replace("]", "")

        link = "<a href=#reference-{id}><sup>[{id}]</sup></a>".format(id=id)

        text = text.replace(match, link)

    return mark_safe(text)