from django.db import models

class users(models.Model):
    uid = models.CharField(max_length=50)
    upw = models.CharField(max_length=50)
    name = models.CharField(max_length=20)