from django.db import models

# Create your models here.
class translation(models.Model):
    user = models.CharField(max_length=50)
    filename = models.CharField(max_length=50)
    comment = models.TextField()
    translation = models.TextField()
