from django.contrib import admin
from main.models import *

class NotebookAdmin(admin.ModelAdmin):
    list_display = ('title',)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('notebook','title','pages')
class PageAdmin(admin.ModelAdmin):
    list_display = ('filename',)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user','story')
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('project','page')

admin.site.register(Notebook,NotebookAdmin)
admin.site.register(Story,StoryAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Translation,TranslationAdmin)
