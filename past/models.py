from django.db import models
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from taggit.models import Tag

# Create your models here.


class Article(models.Model):
	title = models.CharField(max_length=200)
	content = models.CharField(max_length=10000)

	country = CountryField()
	tags = TaggableManager()

	def __unicode__(self):
		return self.title

	def getTagNames(self):
		return self.tags.all()