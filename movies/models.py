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
   title_hash = models.CharField(max_length=200, blank=True)
   filename   = models.CharField(max_length=200, blank=True)
   year       = models.DateTimeField('Movie year')
   director   = models.ForeignKey(Director, on_delete=models.CASCADE)

   def __str__(self):
      return self.year + str() + self.title
   def custom_meth(self):
      return "Voila"
