from django.contrib import admin
from .models import BlogPost, Entry, Topic, Edits

# Register your models here.

admin.site.register(BlogPost)
admin.site.register(Entry)
admin.site.register(Topic)
admin.site.register(Edits)

