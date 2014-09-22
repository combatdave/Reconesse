from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db.models import Q, Max, Min
import json
import datetime

from django_countries import countries
from past.models import Article, PastImage, Category


def get_all_countries():
    """ Returns an array of all countries that have at least one article
    associated with them.

    Elements are on the form {'name', 'code'} """
    codes = Article.objects.all().order_by('country')\
                                 .distinct('country')\
                                 .values_list('country', flat=True)
    country_dict = dict(countries)
    return[{'name': unicode(country_dict[c]), 'code': c} for c in codes]


def index(request, reference = None, slug = None):
    yearData = GetArticleYearRanges()
    
    categories = Category.objects.GetTree()

    context = {}
    context["minYear"] = yearData[0]
    context["maxYear"] = yearData[1]
    context["categories"] = categories
    context["countries"] = get_all_countries()

    if reference:
        try:
            context['article'] = Article.objects.get(reference = reference)
            context['images'] = PastImage.objects\
                                         .filter(article=context['article'])
            context["summary"] = context['article'].summaryLines.split("\n")
            relatedArticles = context['article'].relatedArticles.all().order_by('?')[:3]
            if len(relatedArticles) != 0:
                context["relatedArticles"] = relatedArticles
            context["sameCategoryArticles"] = Article.objects.filter(Q(category__id=context['article'].category.id), ~Q(id=context['article'].id)).order_by('?')[:3]
        except Exception as e:
            context['article'] = 'failed'
    else:
        context['article'] = ''
    return render(request, 'past/map.html', context)


def ViewArticle(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise Http404

    images = PastImage.objects.filter(article=article)
    for i in images:
        print "Image!", i.imageField.url

    context = {}
    context['article'] = article
    context["images"] = images
    context["summary"] = article.summaryLines.split("\n")

    relatedArticles = article.relatedArticles.all()
    if len(relatedArticles) != 0:
        context["relatedArticles"] = relatedArticles

    context["sameCategoryArticles"] = Article.objects.filter(Q(category__id=article.category.id), ~Q(id=article.id))

    return render(request, 'past/article.html', context)


def GetArticleYearRanges():
    earliest = Article.objects.aggregate(Min("birthYear"))["birthYear__min"]
    latest = Article.objects.aggregate(Max("deathYear"))["deathYear__max"]
    now = datetime.datetime.now().year

    if latest > now:
        now = latest

    return earliest, now


def GetMapData(request):
    earliestYear, latestYear = GetArticleYearRanges()

    minYear = request.GET.get('minYear')
    if minYear is not None and minYear != "":
        minYear = int(minYear)
    else:
        minYear = earliestYear
    maxYear = request.GET.get('maxYear')
    if maxYear is not None and maxYear != "":
        maxYear = int(maxYear)
    else:
        maxYear = latestYear

    showAll = request.GET.get("showAll")

    allCategories = Category.objects.all()

    categoryFilter = allCategories
    if showAll != "true":
        filterListParam = request.GET.getlist("filterCategories[]")
        categoryFilter = allCategories.filter(name__in=filterListParam)

    categoryIDs = [category.id for category in categoryFilter]

    if maxYear >= latestYear and minYear <= earliestYear and len(allCategories) == len(categoryFilter):
        allArticles = Article.objects.all()
    else:
        bornInTimePeriod = Q(birthYear__gte=minYear) & Q(birthYear__lte=maxYear)
        diedInTimePeriod = Q(deathYear__gte=minYear) & Q(deathYear__lte=maxYear)
        overlappedTimePeriod = Q(birthYear__lt=minYear) & Q(deathYear__gt=maxYear)
        timeQuery = bornInTimePeriod | diedInTimePeriod | overlappedTimePeriod

        categoryQuery = Q(category__id__in=categoryIDs)

        allArticles = Article.objects.filter(timeQuery & categoryQuery)

    numByCountryCode = {}
    for article in allArticles:
        country = article.country.code
        if country not in numByCountryCode:
            numByCountryCode[country] = 0
        numByCountryCode[country] += 1

    areas = []
    for country, num in numByCountryCode.iteritems():
        countryData = {}
        countryData["id"] = country
        countryData["value"] = num
        areas.append(countryData)

    jsonResponse = {}
    jsonResponse["minYear"] = minYear
    jsonResponse["maxYear"] = maxYear
<<<<<<< HEAD
    #jsonResponse["map"] = "worldLow"
=======
    # jsonResponse["map"] = "worldLow"
>>>>>>> 9abb596fc15e9e41c98e4628f94fd7ca520e5b18
    #jsonResponse["getAreasFromMap"] = False
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
        raise Http404

    context = {}
    context["countryName"] = countryName
    context["articles"] = articlesByCountry
    return render(request, "past/articlelist.html", context)


def Search(request):
    categories = request.GET.getlist("category")
    countrycodes = request.GET.getlist("countrycode")
    keywords = request.GET.getlist("keyword")
    tags = request.GET.getlist("tag")
    minYear = request.GET.get("minyear")
    maxYear = request.GET.get("maxyear")


    earliestPossible, latestPossible = GetArticleYearRanges()
    if minYear is None:
        minYear = earliestPossible
    if maxYear is None:
        maxYear = latestPossible
    countrycodes = [code.upper() for code in countrycodes]

    bornInTimePeriod = Q(birthYear__gte=minYear) & Q(birthYear__lte=maxYear)
    diedInTimePeriod = Q(deathYear__gte=minYear) & Q(deathYear__lte=maxYear)
    overlappedTimePeriod = Q(birthYear__lt=minYear) & Q(deathYear__gt=maxYear)
    timeQuery = bornInTimePeriod | diedInTimePeriod | overlappedTimePeriod

    textQuery = Q()
    for keyword in keywords:
        textQuery = textQuery | (Q(content__icontains=keyword) | Q(title__icontains=keyword))

    countryQuery = Q()
    for countrycode in countrycodes:
        countryQuery = countryQuery | (Q(country__exact=countrycode))

    categoryQuery = Q()
    for category in categories:
        categoryQuery = categoryQuery | Q(category__name__iexact=category)

    tagQuery = Q()
    for tag in tags:
        tagQuery = tagQuery | Q(tags__name__iexact=tag)

    fullQuery = timeQuery & textQuery & countryQuery & categoryQuery & tagQuery

    matches = Article.objects.filter(fullQuery)

    matches = [dict(name=m.title, id=m.id) for m in matches]

    jsonResponse = {}
    jsonResponse["categories"] = categories
    jsonResponse["countryCodes"] = countrycodes
    jsonResponse["keywords"] = keywords
    jsonResponse["minYear"] = minYear
    jsonResponse["maxYear"] = maxYear
    jsonResponse["matches"] = matches
    jsonResponse["tags"] = tags

    return HttpResponse(json.dumps(jsonResponse), content_type="application/json")
