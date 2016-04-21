from __future__ import unicode_literals

from django.db import models

# Create your models here.
class url_a_acortar(models.Model):
    URL = models.CharField(max_length=500)
