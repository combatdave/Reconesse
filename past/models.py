from django.db import models
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from taggit.models import Tag

# Create your models here.


class Article(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	summaryLines = models.TextField()

	birthYear = models.IntegerField(default=0);
	deathYear = models.IntegerField(null=True, blank=True);

	country = CountryField()
	tags = TaggableManager(related_name="past_tags")

	def __unicode__(self):
		return self.title

	def getTagNames(self):
		return self.tags.all()


class PastImage(models.Model):
	imageField = models.ImageField(upload_to="images")
	article = models.ForeignKey(Article)

	def __unicode__(self):
		return "Article: '" + self.article.title + "' - Image: " + self.imageField.url