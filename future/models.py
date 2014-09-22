from django.db import models
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from taggit.models import Tag

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    country = CountryField()
    tags = TaggableManager(related_name="future_tags")

    def __unicode__(self):
        return self.title

    def getTagNames(self):
        return self.tags.all()