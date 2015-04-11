from django.contrib import admin
from django import forms
from future.models import Article, FutureImage

# Register your models here.

class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Article


class FutureImageToArticleInline(admin.TabularInline):
    fk_name = "article"
    model = FutureImage


class RelatedArticlesInline(admin.TabularInline):
    fk_name = "from_article"
    model = Article.relatedArticles.through
    verbose_name = "Related article"
    verbose_name_plural = "Related articles"


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm

    readonly_fields = ("slug", )
    inlines = [FutureImageToArticleInline, RelatedArticlesInline]
    exclude = ("relatedArticles", )


class FutureImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(FutureImage, FutureImageAdmin)