from django.contrib import admin
from django import forms
from future.models import Article

# Register your models here.

class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Article


class ArticleAdmin(admin.ModelAdmin):
	form = ArticleAdminForm

	#fieldsets = [
    #    (None,               {'fields': ['title', 'content']})
    #]


admin.site.register(Article, ArticleAdmin)
