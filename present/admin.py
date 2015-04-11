from django.contrib import admin
from present.models import Entry, PresentImage
from django import forms
from tinymce.widgets import TinyMCE


class EntryAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 160, 'rows': 30}))

    class Meta:
        model = Entry


class EntryAdmin(admin.ModelAdmin):
    form = EntryAdminForm

    readonly_fields = ("slug", "submittedBy", "submittedTime")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.submittedBy = request.user
        obj.save()


class PresentImageAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Entry, EntryAdmin)
admin.site.register(PresentImage, PresentImageAdmin)