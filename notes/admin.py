from django.contrib import admin

from notes.models import Note

# Register your models here.
admin.site.site_header = "NoteMate Admin"
admin.site.site_title = "NoteMate Admin Portal"
admin.site.index_title = "Welcome to NoteMate Admin Portal"

admin.site.register(Note)