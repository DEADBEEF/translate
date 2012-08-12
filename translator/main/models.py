from django.db import models

# Create your models here.
class Translation(models.Model):
    user = models.CharField(max_length=50)
    filename = models.TextField()
    comment = models.TextField()
    translation = models.TextField()

class Notebook(models.Model):
    title = models.CharField(max_length=50,primary_key=True)
    short_title = models.CharField(max_length=10,db_index=True)

class Story(models.Model):
    notebook = models.ForeignKey('Notebook')
    title = models.CharField(max_length=300)
    created = models.CharField(max_length=200)
    description = models.TextField()
    comment = models.TextField()
    contributor = models.TextField()
    subject = models.TextField()
    keyword = models.TextField()

class Page(models.Model):
    story = models.ForeignKey('Story')
    filename = models.TextField()
    uuid = models.CharField(max_length=40,db_index=True)
