from django.contrib import admin
from notes.models import Notes
from . import models

class NotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


admin.site.register(models.Notes, NotesAdmin)