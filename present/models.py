from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    submittedBy = models.ForeignKey(User, editable=False)
    submittedTime = models.DateTimeField(auto_now_add=True, editable=False)
    tags = TaggableManager(related_name="present_tags")


    def __unicode__(self):
        return self.title

    def getTagNames(self):
        return self.tags.all()