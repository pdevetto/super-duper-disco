from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Director(models.Model):
   name = models.CharField(max_length=200)

   def __str__(self):
      return self.name

@python_2_unicode_compatible
class Movie(models.Model):
   title      = models.CharField(max_length=200, blank=True)
   titlehash  = models.CharField(max_length=200)

   filename   = models.CharField(max_length=200, blank=True)
   filepath   = models.CharField(max_length=255, blank=True)

   poster     = models.CharField(max_length=200, blank=True)
   year       = models.DateTimeField('Movie year', null=True)
   director   = models.ForeignKey(Director, on_delete=models.CASCADE, null=True)

   def __str__(self):
      return str(self.year) + ")- "+ self.title + " / " + self.titlehash
   def custom_meth(self):
      return "Voila"
