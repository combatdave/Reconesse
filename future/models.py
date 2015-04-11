from django.db import models
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify


# Create your models here.


class Article(models.Model):
    class Meta:
    #    ordering = ('slug',)
        verbose_name = "article"
        verbose_name_plural = "articles"

    title = models.CharField(max_length=200)
    content = models.TextField()

    country = CountryField()

    relatedArticles = models.ManyToManyField("self", related_name="relatedby")

    tags = TaggableManager(related_name="future_tags")

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
            slug_str = "%s" % (self.title, )
            self.slug = slugify(slug_str)
            self.save()


class FutureImage(models.Model):
    imageField = models.ImageField(upload_to="images")
    article = models.ForeignKey(Article)

    def __unicode__(self):
        return "Article: '" + self.article.title + "' - Image: " + self.imageField.url