from django.core.management.base import BaseCommand, CommandError
import random
from past.models import Article, Category, PastReference
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

loremIpsum = "Lorem ipsum dolor sit amet[1], consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n\n"

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


references = """lobortis risus. In mi pede, nonummy ut,	Giselle T. Fuller	2014
vel, mauris. Integer sem	Ava L. Harding	2014
elit, a feugiat	Casey M. Maxwell	2014
Curabitur vel lectus. Cum sociis natoque penatibus	Bryar D. Dunn	2014
Duis gravida. Praesent	Hyatt S. Salinas	2014
amet, dapibus id, blandit at, nisi.	Oscar U. Hoover	2015
dui augue eu tellus.	Len T. Woodward	2013
Nunc mauris sapien,	Sade O. Compton	2015
viverra. Donec tempus, lorem fringilla ornare	Alisa Y. Banks	2015
facilisis vitae, orci. Phasellus dapibus	Susan W. Mcclure	2015
Mauris eu turpis. Nulla aliquet. Proin velit. Sed	Drew H. Carter	2015
ac ipsum. Phasellus vitae mauris sit amet lorem	Kasper K. Bauer	2014
id magna et ipsum cursus vestibulum. Mauris	Blake N. Larson	2014
lacus, varius et, euismod et,	Jordan Y. Gray	2014
neque. In ornare sagittis felis.	Chaney G. Mercer	2014
ornare, elit elit fermentum risus, at fringilla purus	Maryam T. Sweet	2013
diam eu dolor egestas rhoncus. Proin nisl	Kyla M. Wilkinson	2013
orci lacus vestibulum lorem, sit	Caleb E. Mueller	2015
vel nisl. Quisque fringilla euismod	Tamekah Z. Marsh	2015
enim, sit amet ornare lectus justo eu	Raya O. Decker	2014"""
referenceList = references.replace("\t", " - ").split("\n")

tags = "#money #cash #green #TagsForLikes #dough #bills #crisp #benjamin #benjamins #franklin #franklins #bank #payday #hundreds #twentys #fives #ones #100s #20s #greens #photooftheday #instarich #instagood #capital #stacks #stack #bread #paid"
tagsList = tags.replace("#", "").split()

categories = Category.objects.all()
categogies = [c for c in categories if c.parent is not None]

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

    a = Article(title=articleName, content=articleText, summaryLines=articleSummaryLines, birthYear=birthYear,
                deathYear=deathYear, country=randomCountry, category=randomCategory)
    a.save()
    for i in range(1, random.randint(2, 5)):
        a.tags.add(random.choice(tagsList))

    allArticles = Article.objects.all()
    for i in range(0, random.randint(0, 3)):
        a.relatedArticles.add(random.choice(allArticles))

    for i in range(1, 5):
        ref = PastReference(text = random.choice(referenceList), url="http://www.google.com/", article=a)
        ref.save()

    print "Inserted ", a


class Command(BaseCommand):
    args = '<num entiries>'
    help = 'Creates a number of random entries'

    def handle(self, *args, **options):
        num = args[0]
        num = int(num)
        for i in xrange(num):
            CreateRandomEntry()

        print "Done"