from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.db.models import Q, Avg, Max, Min
import json
import datetime

from django_countries import countries
from past.models import Article, PastImage, Category

# Create your views here.
def index(request):
	yearData = GetArticleYearRanges()

	categories = Category.objects.GetTree()
	print categories

	context = {}
	context["minYear"] = yearData[0]
	context["maxYear"] = yearData[1]
	context["categories"] = categories

	return render(request, 'past/map.html', context)


def ViewArticle(request, articleID):
	article = None
	try:
		article = Article.objects.get(id=articleID)
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
	queryResult = Article.objects.aggregate(Min("birthYear"))

	earliest = queryResult["birthYear__min"]
	now = datetime.datetime.now().year

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
	categoryFilter = allCategories;
	if showAll != "true":
		filterListParam = request.GET.getlist("filterCategories[]")
		print "not showAll, filterListParam =", filterListParam
		categoryFilter = allCategories.filter(name__in=filterListParam)

	categoryIDs = [category.id for category in categoryFilter]
	categoryIDsString = str(tuple(categoryIDs))
	if len(categoryIDs) == 1:
		categoryIDsString = categoryIDsString.replace(",", "")

	if maxYear >= latestYear and minYear <= earliestYear and len(allCategories) == len(categoryFilter):
		allArticles = Article.objects.all()
	else:
		query = """
		SELECT * FROM past_article

		WHERE
		(
			(birthYear >= {minYear} AND birthYear <= {maxYear})
			OR
			(deathYear >= {minYear} AND deathYear <= {maxYear})
			OR
			(birthYear < {minYear} AND deathYear > {maxYear})
		)	
		AND
		(
			category_id IN {categoryIDs}
		)
		""".format(minYear = minYear, maxYear = maxYear, categoryIDs = categoryIDsString)

		allArticles = Article.objects.raw(query)

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
		articlesByCountry = None
		raise Http404

	context = {}
	context["countryName"] = countryName
	context["articles"] = articlesByCountry
	return render(request, "past/articlelist.html", context)

	#return HttpResponse("Got {0} articles for {1} ({2})".format(len(articlesByCountry), unicode(countryName), countryCode))