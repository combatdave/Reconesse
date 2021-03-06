from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db.models import Q, Max, Min
import json
import datetime
from django.views.decorators.csrf import csrf_exempt

from django_countries import countries
from past.models import Article, PastImage, Category, PastReference


def get_all_countries():
    """ Returns an array of all countries that have at least one article
    associated with them.

    Elements are on the form {'name', 'code'} """
    codes = Article.objects.all().order_by('country')\
                                 .values_list('country', flat=True)
    codes = set(codes)  # .distinct doesnt work with mysql db
    country_dict = dict(countries)
    return sorted([{'name': unicode(country_dict[c]), 'code': c} for c in codes],
                   key=lambda k: k['name'])


def index(request, slug = None):
    yearData = GetArticleYearRanges()

    context = {}
    context["minYear"] = yearData[0]
    context["maxYear"] = yearData[1]
    context["categories"] = Category.objects.GetTree()
    context["countries"] = get_all_countries()

    if slug:
        try:
            context['article'] = Article.objects.get(slug = slug)
            context['images'] = PastImage.objects\
                                         .filter(article=context['article'])
            context['references'] = PastReference.objects.filter(article=context['article']).order_by('id')
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

def profile(request, slug):
    context = {}
    try:
        context['article'] = Article.objects.get(slug = slug)
        context['images'] = PastImage.objects\
                                     .filter(article=context['article'])
        context['references'] = PastReference.objects\
                                             .filter(article=context['article'])\
                                             .order_by('id')
        context['summary'] = context['article'].summaryLines.split('\n')
        relatedArticles = context['article'].relatedArticles.all().order_by('?')[:3]
        if len(relatedArticles) != 0:
            context['relatedArticles'] = relatedArticles
        context['sameCategoryArticles'] = Article.objects.filter(Q(category__id=context['article'].category.id), ~Q(id=context['article'].id)).order_by('?')[:3]
    except Exception as e:
        context['article'] = 'failed'
    return render(request, 'past/profile.html', context)

def feed(request):
    yearData = GetArticleYearRanges()

    context = {}
    context["minYear"] = yearData[0]
    context["maxYear"] = yearData[1]
    context["categories"] = Category.objects.GetTree()
    context["countries"] = get_all_countries()

    return render(request, 'past/feed.html', context)


def ViewArticle(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise Http404

    images = PastImage.objects.filter(article=article)
    references = PastImage.objects.filter(article=article)

    context = {}
    context['article'] = article
    context["images"] = images
    context["references"] = references
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


def _ArticleListToListOfDicts(profiles):
    return [dict(id=m.id,
                name=m.title,
                slug=m.slug,
                country=m.country.code,
                birth=m.birthYear,
                death=m.deathYear,
                deathYearUnknown=m.deathYearUnknown,
                summary=m.summaryLines,
                tags=[str(t) for t in m.tags.all()]) for m in profiles]


def _GetMatches(categories, countrycodes, keywords, tags, minYear, maxYear, startIndex=0, numToReturn=0):
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

    matches = Article.objects.filter(fullQuery)

    matches = matches[startIndex:]
    if numToReturn > 0:
        matches = matches[:numToReturn]

    matches = _ArticleListToListOfDicts(matches)

    # Attach an image to each article
    for m in matches:
        try:
            img = PastImage.objects.filter(article_id=m['id'])
            if img.exists():
                m['image'] = str(img.get().imageField.url)
                print m['image']
        except Exception as e:
            print(e)

    return matches


@csrf_exempt
def GetArticles(request):
    searchJSON = request.POST.get("query", "{}")
    searchParams = json.loads(searchJSON)

    categories = searchParams.get("categories", [])
    countrycodes = searchParams.get("countrycodes", [])

    print(categories)
    print(countrycodes)
    keywords = searchParams.get("keywords", [])
    tags = searchParams.get("tags", [])
    minYear = searchParams.get("minyear", "")
    maxYear = searchParams.get("maxyear", "")
    startIndex = searchParams.get("startindex", 0)
    numToReturn = searchParams.get("num", 0)

    matches = _GetMatches(categories, countrycodes, keywords, tags, minYear, maxYear, startIndex, numToReturn)

    response = {}
    response["query"] = searchParams
    response["results"] = matches

    return HttpResponse(json.dumps(response), content_type="application/json")


def Search(request):
    categories = json.loads(request.POST.get("category", []))
    countrycodes = json.loads(request.POST.get("countrycode", []))
    keywords = json.loads(request.POST.get("keyword", []))
    tags = json.loads(request.POST.get("tag", []))
    minYear = request.POST.get("minyear", '')
    maxYear = request.POST.get("maxyear", '')

    matches = _GetMatches(categories, countrycodes, keywords, tags, minYear, maxYear)

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
        "tags"          : tags,
        "areas"         : areas,
        "articles"      : articlesByCountryCode
    }
    return HttpResponse(json.dumps(jsonResponse), content_type="application/json")


def TagSearch(request):
    tag = request.GET.get("tag", '')

    articlesWithThisTag = Article.objects.filter(tags__name__in=[tag, ])
    articlesWithThisTag = _ArticleListToListOfDicts(articlesWithThisTag)

    jsonResponse = {
        "tag": tag,
        "articles": articlesWithThisTag,
    }
    return HttpResponse(json.dumps(jsonResponse), content_type="application/json")


# Don't mind me
def GenerateImage(request):
    import random
    women = [
        'http://www.howtogetthewomanofyourdreams.com/wp-content/uploads/2013/03/womanslide21.png',
        'http://reneemullingslewis.com/wp-content/uploads/2014/08/woman-smiling.png',
        'http://dreamatico.com/data_images/woman/woman-2.jpg',
        'http://www.wonderslist.com/wp-content/uploads/2015/10/Doutzen-Kroes-Most-Beautiful-Dutch-Woman.jpg',
        'http://dreamatico.com/data_images/woman/woman-3.jpg',
        'http://womensbusiness.info/wp-content/uploads/2014/10/v1-woman.png',
        'http://neimandermatology.com/wp-content/uploads/2014/11/Cosmetic-Woman.png'
    ]

    articles = Article.objects.all()

    for a in articles:
        PastImage.objects.create(article_id = a.id, imageField = random.choice(women))

    return HttpResponse('Images generated')
