from django.contrib import admin
from django import forms
from django.utils.html import conditional_escape, mark_safe
from django.utils.encoding import smart_text
from django.forms import TextInput, Textarea
from django.db import models

from past.models import Article, PastImage, Category, PastReference


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
            parentEntry = (self.prepare_value(parent), self.label_from_instance(parent))
            choices.append(parentEntry)

            choices.extend(self.get_child_list(parent))

        self.choices = choices


    def get_child_list(self, parent):
        choices = []
        children = getattr(parent, self.related_name).all()
        for child in children:
            choice = (self.prepare_value(child), self.label_from_instance(child))
            choices.append(choice)

            childChoices = self.get_child_list(child)
            choices.extend(childChoices)

        return choices


    def label_from_instance(self, obj):
        level_indicator = ""

        parent = getattr(obj, self.parent_field, None)
        while parent is not None:
            level_indicator += "--- "
            parent = getattr(parent, self.parent_field, None)

        return mark_safe(level_indicator + conditional_escape(smart_text(getattr(obj, self.label_field))))


class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)
        self.fields["category"] = NestedModelChoiceField(queryset=Category.objects.all(), related_name="parentcategory",
                                                         parent_field="parent", label_field="name")

    def clean_category(self):
        category = self.cleaned_data['category']
        if category.parent is None:
            raise forms.ValidationError("You can't select a top-level category! For example instead of \"arts\", try \"painter\".")
        return category

    class Meta:
        model = Article


class PastImageToArticleInline(admin.TabularInline):
    fk_name = "article"
    model = PastImage


class CategoryToCategoryInline(admin.TabularInline):
    fk_name = "parent"
    model = Category


class RelatedArticlesInline(admin.TabularInline):
    fk_name = "from_article"
    model = Article.relatedArticles.through
    verbose_name = "Related article"
    verbose_name_plural = "Related articles"


class PastReferenceToArticleInline(admin.TabularInline):
    fk_name = "article"
    model = PastReference

    formfield_overrides = {
            models.TextField: {'widget': TextInput(attrs={'size': '100'})},
        }


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm

    readonly_fields = ("slug", )
    inlines = [PastReferenceToArticleInline, PastImageToArticleInline, RelatedArticlesInline, ]
    exclude = ("relatedArticles", )


class PastImageAdmin(admin.ModelAdmin):
    pass


class PastReferenceAdmin(admin.ModelAdmin):
    pass


class CategoryAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryAdminForm, self).__init__(*args, **kwargs)
        self.fields["parent"] = NestedModelChoiceField(queryset=Category.objects.all(), related_name="parentcategory",
                                                       parent_field="parent", label_field="name", required=False,
                                                       empty_label="None (add new root category)")

    class Meta:
        model = Category


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    inlines = [CategoryToCategoryInline]


admin.site.register(Article, ArticleAdmin)
admin.site.register(PastImage, PastImageAdmin)
admin.site.register(Category, CategoryAdmin)