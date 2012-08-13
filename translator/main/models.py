from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notebook(models.Model):
    title = models.CharField(max_length=50,primary_key=True)
    short_title = models.CharField(max_length=10,db_index=True)

class Story(models.Model):
    notebook = models.ForeignKey(Notebook)
    title = models.CharField(max_length=300)
    created = models.CharField(max_length=200)
    description = models.TextField()
    comment = models.TextField()
    contributor = models.TextField()
    subject = models.TextField()
    keyword = models.TextField()
    pages = models.IntegerField()
    def __unicode__(self):
        return self.title

class Page(models.Model):
    story = models.ForeignKey(Story)
    filename = models.TextField()
    uuid = models.CharField(max_length=40,db_index=True)

class Project(models.Model):
    user = models.ForeignKey(User)
    story = models.ForeignKey(Story)
    notes = models.TextField()

class Translation(models.Model):
    project = models.ForeignKey(Project)
    page = models.ForeignKey(Page)
    notes = models.TextField()
    translation = models.TextField()
    done = models.BooleanField()
