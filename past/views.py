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
                                 .values_list('country', flat=True)
    codes = set(codes)  # .distinct doesnt work with mysql db
    country_dict = dict(countries)
    return[{'name': unicode(country_dict[c]), 'code': c} for c in codes]


def index(request, slug = None):
    yearData = GetArticleYearRanges()
    
    categories = Category.objects.GetTree()

    context = {}
    context["minYear"] = yearData[0]
    context["maxYear"] = yearData[1]
    context["categories"] = categories
    context["countries"] = get_all_countries()

    if slug:
        try:
            context['article'] = Article.objects.get(slug = slug)
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
    #jsonResponse["map"] = "worldLow"
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
    categories = request.POST.getlist("category", [])
    countrycodes = request.POST.getlist("countrycode", [])
    keywords = request.POST.getlist("keyword", [])
    tags = request.POST.getlist("tag", '')
    minYear = request.POST.get("minyear", '')
    maxYear = request.POST.get("maxyear", '')

    earliestPossible, latestPossible = GetArticleYearRanges()
    if not minYear:
        minYear = earliestPossible
    if not maxYear:
        maxYear = latestPossible
    countrycodes = [code.upper() for code in countrycodes]

    bornInTimePeriod = Q(birthYear__gte=minYear) & Q(birthYear__lte=maxYear)
    diedInTimePeriod = Q(deathYear__gte=minYear) & Q(deathYear__lte=maxYear)
    overlappedTimePeriod = Q(birthYear__lt=minYear) & Q(deathYear__gt=maxYear)
    timeQuery = bornInTimePeriod | diedInTimePeriod | overlappedTimePeriod
    
    fullQuery = timeQuery

    if keywords != ['']:
        textQuery = Q()
        for keyword in keywords:
            textQuery = textQuery |\
                        (Q(content__icontains=keyword) |\
                         Q(title__icontains=keyword))
        fullQuery = fullQuery & textQuery

    if countrycodes != ['']:
        countryQuery = Q()
        for countrycode in countrycodes:
            countryQuery = countryQuery | (Q(country__exact=countrycode))
        fullQuery = fullQuery & countryQuery

    if categories != ['']:
        categoryQuery = Q()
        for category in categories:
            categoryQuery = categoryQuery | Q(category__name__iexact=category)
        fullQuery = fullQuery & categoryQuery

    if tags != ['']:
        tagQuery = Q()
        for tag in tags:
            tagQuery = tagQuery | Q(tags__name__iexact=tag)
        fullQuery = fullQuery & tagQuery

    #fullQuery = timeQuery & textQuery & countryQuery & categoryQuery & tagQuery

    matches = Article.objects.filter(fullQuery)

    matches = [dict(name=m.title,
                    slug=m.slug,
                    country=m.country.code,
                    birth=m.birthYear,
                    death=m.deathYear,
                    tags=[str(t) for t in m.tags.all()]) for m in matches]
 
    numByCountryCode = {}
    articlesByCountryCode = {}
    for article in matches:
        country = article['country']
        if country not in numByCountryCode:
            numByCountryCode[country] = 0
        numByCountryCode[country] += 1
        if country not in articlesByCountryCode:
            articlesByCountryCode[country] = []
        articlesByCountryCode[country].append(article)
    
    areas = []
    for country, num in numByCountryCode.iteritems():
        countryData = {}
        countryData["id"] = country
        countryData["value"] = num
        areas.append(countryData)

    jsonResponse = {
        "categories"    : categories,
        "countryCodes"  : countrycodes,
        "keywords"      : keywords,
        "minYear"       : minYear,
        "maxYear"       : maxYear,
        #"matches"       : matches,
        "tags"          : tags,
        "areas"         : areas,
        "articles"      : articlesByCountryCode
    }
    return HttpResponse(json.dumps(jsonResponse), content_type="application/json")
