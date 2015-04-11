from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.template.defaultfilters import slugify


class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()

    submittedBy = models.ForeignKey(User, editable=False)
    submittedTime = models.DateTimeField(auto_now_add=True, editable=False)
    tags = TaggableManager(related_name="present_tags")

    slug = models.SlugField(blank=True)


    def __unicode__(self):
        return self.title

    def getTagNames(self):
        return self.tags.all()


    def save(self, *args, **kwargs):
        """ We redefine the save method to create a unique slug number upon
        being called for the first time on any Article """
        created = not self.pk
        super(Entry, self).save(*args, **kwargs)
        if created:
            slug_str = "%s %s" % (self.title, self.submittedTime.strftime('%Y-%m-%d-%H-%M'))
            self.slug = slugify(slug_str)
            self.save()


class PresentImage(models.Model):
    name = models.CharField(max_length=100)
    imageField = models.ImageField(upload_to="images\present")

    def __unicode__(self):
        return self.name + " - " + self.imageField.url