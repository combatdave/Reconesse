from django.contrib import admin
from present.models import Entry

class EntryAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
	    if not change:
	        obj.submittedBy = request.user
	    obj.save()

# Register your models here.
admin.site.register(Entry, EntryAdmin)