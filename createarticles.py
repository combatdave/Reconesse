import os
os.environ["DJANGO_SETTINGS_MODULE"] =  "Reconesse.settings"

import random
from past.models import Article, Category
from django_countries import countries

allNames = """Juliana Rizzuto
Devona Leak
Suzanna Deeb
Charlyn Gaillard
Hyun Gannaway
Indira Felker
Gertude Toscano
Violeta Shalash
Larue Whang
Mellie Whitlatch
Tina Hubne
Blanch Bounds
Viviana Welt
Lizbeth Isham
Georgene Ellefson
Karoline Michelson
Taina Sang
Mignon Morquecho
Henriette Lineberry
Natacha Orrell
Rosette Degregorio
Margaret Laviolette
Tonisha Oropeza
Jannet Stricklin
Hallie Jorstad
Bobbye Huson
Olimpia Duhon
Rhea Shunk
Laraine Ortis
Luvenia Hogue
Reta Hussain
Bertie Lipari
Julee Wellborn
Dixie Barcia
Mayra Celentano
Lorriane Mcknight
Bryanna Pattison
Kirstin Bjornstad
Viva Hammes
Yung Stecher
Billye Tatman
Shanice Maglione
Jerica Laufer
Exie Shelor
Evangeline Foley
Lisette Toma
Tia Nitz
Tanja Dau
Candi Burke
Angeline Neel"""
nameList = allNames.split("\n")
firstNames = [name.split()[0] for name in nameList]
lastNames = [name.split()[1] for name in nameList]

loremIpsum = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n\n"

achievements = """Met deadlines consistently
Reined in rollercoaster project X
Supervised large/complex project in attaining goal X
Grew customer base by X amount
Grew donor base by X amount
Multiplied donations by X %
Cut costs by X amount within Y amount of time
Launched X new websites/products/campaigns
Increased portfolio earnings by X %
Integrated an extremely complex system for the company
United multiple teams post-merger
Finished sales quota X amount of time early
Reduced client/reader attrition by X amount
Met X national/global/industry standard within Y amount of time"""
achievementList = achievements.split("\n")

tags = "#money #cash #green #TagsForLikes #dough #bills #crisp #benjamin #benjamins #franklin #franklins #bank #payday #hundreds #twentys #fives #ones #100s #20s #greens #photooftheday #instarich #instagood #capital #stacks #stack #bread #paid"
tagsList = tags.split()

categories = Category.objects.all()	


if len(categories) == 0:
	raise Exception("No categories! Go make some.")

def CreateRandomEntry():
	articleName = random.choice(firstNames) + " " + random.choice(lastNames)
	articleText = loremIpsum * random.randint(1, 10)
	articleSummaryLines = "\n".join([random.choice(achievementList) for i in xrange(1, random.randint(2, 5))])
	birthYear = random.randint(-1000, 2014)
	deathYear = birthYear + random.randint(20, 90)
	if deathYear > 2014:
		deathYear = None

	randomCountry = random.choice(list(countries))[0]

	randomCategory = random.choice(categories)

	a = Article(title=articleName, content=articleText, summaryLines=articleSummaryLines, birthYear=birthYear, deathYear=deathYear, country=randomCountry, category=randomCategory)
	a.save()
	for i in range(1, random.randint(2, 5)):
		a.tags.add(random.choice(tagsList))

	allArticles = Article.objects.all()
	for i in range(0, random.randint(0, 3)):
		a.relatedArticles.add(random.choice(allArticles))

	print "Inserted ", a


for i in xrange(10):
	CreateRandomEntry()

print "Done"
