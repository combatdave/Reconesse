from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.db.models import Q
import json

from django_countries import countries
from present.models import Entry

# Create your views here.
def index(request):
    context = {}

    entries = Entry.objects.all()
    context["entries"] = entries

    return render(request, 'present/blog.html', context)


def ViewEntry(request, entryID):
    entry = None
    try:
        entry = Entry.objects.get(id=entryID)
    except Entry.DoesNotExist:
        raise Http404

    context = {'entry': entry}
    return render(request, 'present/entry.html', context)