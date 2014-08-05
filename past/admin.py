from django.contrib import admin
from django import forms
from past.models import Article, PastImage

# Register your models here.

class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Article


class PastImageToArticleInline(admin.TabularInline):
	fk_name = "article"
	model = PastImage


class ArticleAdmin(admin.ModelAdmin):
	form = ArticleAdminForm

	#fieldsets = [
    #    (None,               {'fields': ['title', 'content']})
    #]
	inlines = [PastImageToArticleInline]


class PastImageAdmin(admin.ModelAdmin):
	pass

admin.site.register(Article, ArticleAdmin)
admin.site.register(PastImage, PastImageAdmin)