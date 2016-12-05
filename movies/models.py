from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

DIRECTOR = 0
ACTOR = 1
PRODUCER = 2
PEOPLE_ROLE = ((DIRECTOR, 'Director'), (ACTOR, 'Actor'), (PRODUCER, 'Producer'))

@python_2_unicode_compatible
class People(models.Model):
   name     = models.CharField(max_length=200)
   tmdb_id  = models.IntegerField(blank=True)
   def __str__(self):
      return self.name

@python_2_unicode_compatible
class Movie(models.Model):
   title      = models.CharField(max_length=200, blank=True)
   titlehash  = models.CharField(max_length=200)

   filename   = models.CharField(max_length=200, blank=True)
   filepath   = models.CharField(max_length=255, blank=True)

   poster     = models.CharField(max_length=200, blank=True)
   year       = models.IntegerField(blank=True)
   tmdb_id    = models.IntegerField(blank=True)

   def __str__(self):
      return str(self.year) + ")- "+ self.title + " / " + self.titlehash
   def custom_meth(self):
      return "Voila"

@python_2_unicode_compatible
class Role(models.Model):
   role = models.IntegerField(default=0, choices=PEOPLE_ROLE)
   people = models.ForeignKey(People, on_delete=models.CASCADE, null=True)
   movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)

   def __str__(self):
      return self.name
