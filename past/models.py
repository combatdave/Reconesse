from django.db import models
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
#from utils import unique_slugify
from django.template.defaultfilters import slugify

import urlutils


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
    class Meta:
        ordering = ('slug',)

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

    def save(self, *args, **kwargs):
        """ We redefine the save method to create a unique slug number upon
        being called for the first time on any Article """
        created = not self.pk
        super(Article, self).save(*args, **kwargs)
        if created:
            slug_str = "%s %s %s" % (self.title,
                                     self.birthYear,
                                     self.deathYear\
                                     if self.deathYear is not None else "")
            self.slug = slugify(slug_str)
            self.save()


class PastImage(models.Model):
    imageField = models.ImageField(upload_to="images")
    article = models.ForeignKey(Article)

    def __unicode__(self):
        return "Article: '" + self.article.title + "' - Image: " + self.imageField.url
