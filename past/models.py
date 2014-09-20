from django.db import models
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from utils import unique_slugify


class CategoryManager(models.Manager):
    def GetRoots(self):
        topLevel = self.filter(parent__isnull=True)
        return topLevel


    def GetTree(self):
        roots = self.GetRoots()

        tree = []

        for root in roots:
            children = self.filter(parent__id=root.id)
            branch = [root, children]
            tree.append(branch)

        return tree


    def GetOrdered(self):
        tree = self.GetTree()
        ordered = []
        for branch in tree:
            ordered.append(branch[0])
            ordered += branch[1]

        return ordered


class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="parentcategory")

    objects = CategoryManager()

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summaryLines = models.TextField()

    birthYear = models.IntegerField(default=0);
    deathYear = models.IntegerField(null=True, blank=True);

    country = CountryField()

    relatedArticles = models.ManyToManyField("self", related_name="relatedby")

    category = models.ForeignKey(Category, related_name="category")
    tags = TaggableManager(related_name="past_tags")

    slug = models.SlugField(blank=True)

    def __unicode__(self):
        return self.title

    def getTagNames(self):
        return self.tags.all()

    def save(self, **kwargs):
        slug_str = "%s %s %s %s" % (self.title, self.country, self.birthYear, self.deathYear if self.deathYear is not None else "")
        unique_slugify.unique_slugify(self, slug_str)
        super(Article, self).save(**kwargs)


class PastImage(models.Model):
    imageField = models.ImageField(upload_to="images")
    article = models.ForeignKey(Article)

    def __unicode__(self):
        return "Article: '" + self.article.title + "' - Image: " + self.imageField.url
