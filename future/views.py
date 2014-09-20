from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.db.models import Q
import json

from django_countries import countries
from future.models import Article

# Create your views here.
def index(request):
    context = {}
    context["minYear"] = -100
    context["maxYear"] = 2014

    return render(request, 'future/map.html', context)


def ViewArticle(request, articleID):
    article = None
    try:
        article = Article.objects.get(id=articleID)
    except Article.DoesNotExist:
        raise Http404

    context = {'article': article}
    return render(request, 'future/article.html', context)


def GetMapData(request):
    allArticles = Article.objects.all()

    numByCountryCode = {}
    for article in allArticles:
        country = article.country.code
        if country not in numByCountryCode:
            numByCountryCode[country] = 0
        numByCountryCode[country] += 1

    areas = []
    for country, num in numByCountryCode.iteritems():
        print country, num
        countryData = {}
        countryData["id"] = country
        countryData["value"] = num
        areas.append(countryData)

    jsonResponse = {}
    jsonResponse["map"] = "worldLow"
    jsonResponse["getAreasFromMap"] = True
    jsonResponse["areas"] = areas

    return HttpResponse(json.dumps(jsonResponse), content_type="application/json")


def GetCountryArticles(request, countryCode):
    countryCode = countryCode.upper()

    try:
        countryName = dict(countries)[countryCode]
    except KeyError:
        raise Http404

    articlesByCountry = Article.objects.filter(country__exact=countryCode)
    if len(articlesByCountry) == 0:
        articlesByCountry = None

    context = {}
    context["countryName"] = countryName
    context["articles"] = articlesByCountry
    return render(request, "future/articlelist.html", context)

    # return HttpResponse("Got {0} articles for {1} ({2})".format(len(articlesByCountry), unicode(countryName), countryCode))