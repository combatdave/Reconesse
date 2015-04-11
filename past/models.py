from django.db import models
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify


class CategoryManager(models.Manager):
    def GetRoots(self):
        topLevel = self.filter(parent__isnull=True).order_by("name")
        return topLevel


    def _GetTreeForRoot(self, root):
        tree = []

        children = self.filter(parent__id=root.id).order_by("name")
        for child in children:
            tree.append(child)
            subTree = self._GetTreeForRoot(child)
            if subTree and len(subTree) > 0:
                tree.append(subTree)

        return tree


    def GetTree(self):
        roots = self.GetRoots()

        tree = []

        for root in roots:
            children = self._GetTreeForRoot(root)
            tree.append([root, children])

        return tree


class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey("self",
                               null=True,
                               blank=True,
                               related_name="parentcategory")

    objects = CategoryManager()

    def __unicode__(self):
        return self.name


class Article(models.Model):
    class Meta:
        ordering = ('slug',)
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    title = models.CharField(max_length=200)
    content = models.TextField()
    summaryLines = models.TextField()

    birthYear = models.IntegerField(default=0)
    deathYear = models.IntegerField(null=True, blank=True)
    deathYearUnknown = models.BooleanField(default=False)

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


class PastReference(models.Model):
    class Meta:
        verbose_name = "Reference (be careful when deleting!)"
        verbose_name_plural = "References (be careful when deleting these!)"
    text = models.TextField()
    url = models.TextField(null=True, blank=True)

    article = models.ForeignKey(Article)

    def __unicode__(self):
        referencesForThisArticle = [ref.id for ref in PastReference.objects.filter(article=self.article).order_by('id')]
        if self.id in referencesForThisArticle:
            myIndex = referencesForThisArticle.index(self.id) + 1
        else:
            myIndex = "??"
        return "Reference [{0}]".format(myIndex)
