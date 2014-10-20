from django import template
from django.utils.safestring import mark_safe

import re

register = template.Library()


@register.filter(name='addReferences')
def addReferences(text):
    """Turns all instances of [1] into the link to that reference"""
    regexMatch = re.compile(r'(\[\d+\])')
    for match in regexMatch.findall(text):
        id = match.replace("[", "").replace("]", "")

        link = "<a href=#reference-{id}><sup>[{id}]</sup></a>".format(id=id)

        text = text.replace(match, link)

    return mark_safe(text)


def _UnwravelCategories(categories):
    output = []
    startedli = False

    for i, cat in enumerate(categories):
        if type(cat) is list:
            output.append(["startol", None])
            output.extend(_UnwravelCategories(cat))
            output.append(["stopol", None])
        else:
            if startedli:
                startedli = False
                output.append(["stopli", None])

            output.append(["startli", None])
            startedli = True

            hasChildren = i+1 < len(categories) and\
                          type(categories[i+1]) is list and\
                          categories[i+1] != []
            output.append([cat.name, hasChildren])

    if startedli:
        output.append(["stopli", None])

    return output


@register.filter(name='nestCategories')
def nestCategories(categories):
    return _UnwravelCategories(categories)