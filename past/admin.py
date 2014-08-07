from django.contrib import admin
from django import forms
from django.utils.html import conditional_escape, mark_safe
from django.utils.encoding import smart_text

from past.models import Article, PastImage, Category


class NestedModelChoiceField(forms.ModelChoiceField):
	"""A ModelChoiceField that groups parents and childrens"""
	def __init__(self, related_name, parent_field, label_field, *args, **kwargs):
		super(NestedModelChoiceField, self).__init__(*args, **kwargs)
		self.related_name = related_name
		self.parent_field = parent_field
		self.label_field = label_field
		self._populate_choices()

	def _populate_choices(self):
		# This is *hackish* but simpler than subclassing ModelChoiceIterator
		choices = [(u"", self.empty_label)]
		kwargs = {self.parent_field: None, }
		queryset = self.queryset.filter(**kwargs).prefetch_related(self.related_name)

		for parent in queryset:
			choices.append((self.prepare_value(parent), self.label_from_instance(parent)))
			choices.extend([(self.prepare_value(children), self.label_from_instance(children)) for children in getattr(parent, self.related_name).all()])

		self.choices = choices

	def label_from_instance(self, obj):
		level_indicator = ""
		if getattr(obj, self.parent_field):
			level_indicator = "--- "

		return mark_safe(level_indicator + conditional_escape(smart_text(getattr(obj, self.label_field))))


class ArticleAdminForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea)

	def __init__(self, *args, **kwargs):
		super(ArticleAdminForm, self).__init__(*args, **kwargs)
		self.fields["category"] = NestedModelChoiceField(queryset=Category.objects.all(), related_name="parentcategory", parent_field="parent", label_field="name")

	class Meta:
		model = Article


class PastImageToArticleInline(admin.TabularInline):
	fk_name = "article"
	model = PastImage


class CategoryToCategoryInline(admin.TabularInline):
	fk_name = "parent"
	model = Category


class ArticleAdmin(admin.ModelAdmin):
	form = ArticleAdminForm



	#fieldsets = [
    #    (None,               {'fields': ['title', 'content']})
    #]
	inlines = [PastImageToArticleInline]


class PastImageAdmin(admin.ModelAdmin):
	pass


class CategoryAdminForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CategoryAdminForm, self).__init__(*args, **kwargs)
		self.fields["parent"] = NestedModelChoiceField(queryset=Category.objects.all(), related_name="parentcategory", parent_field="parent", label_field="name", required=False, empty_label="None (add new root category)")

	class Meta:
		model = Category


class CategoryAdmin(admin.ModelAdmin):
	form = CategoryAdminForm
	inlines = [CategoryToCategoryInline]


admin.site.register(Article, ArticleAdmin)
admin.site.register(PastImage, PastImageAdmin)
admin.site.register(Category, CategoryAdmin)