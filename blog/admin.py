from django.contrib import admin
from . import models
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['date_time']
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['__str__', 'author', 'date_time']
    list_filter = ['author', 'post_tags']

admin. site. register(models.Post_Model, PostAdmin)
admin. site. register(models.Post_Tag)
