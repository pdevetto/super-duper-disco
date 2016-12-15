from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

DIRECTOR = 0
ACTOR = 1
PRODUCER = 2
SCREENPLAY = 3
PHOTOGRAPHY = 4
WRITER = 5
PEOPLE_ROLE = (
   (DIRECTOR, 'Director'),
   (ACTOR, 'Actor'),
   (PRODUCER, 'Producer'),
   (SCREENPLAY, 'Screenplay'),
   (PHOTOGRAPHY, 'Director of Photography'),
   (WRITER, 'Writer')
)

@python_2_unicode_compatible
class People(models.Model):
   name     = models.CharField(max_length=200)
   tmdb_id  = models.IntegerField(blank=True)
   profile  = models.CharField(max_length=200, null=True)

   def __str__(self):
      return self.name

@python_2_unicode_compatible
class Genre(models.Model):
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

   poster     = models.CharField(max_length=200, null=True)
   year       = models.IntegerField(null=True)
   tmdb_id    = models.IntegerField(null=True)

   clean      = models.IntegerField(null=True, default=0)
   possible   = models.TextField(null=True)

   genres     = models.ManyToManyField(Genre)

   def __str__(self):
      return self.title
   def custom_meth(self):
      return "Voila"

@python_2_unicode_compatible
class Role(models.Model):
   role     = models.IntegerField(default=0, choices=PEOPLE_ROLE)
   people   = models.ForeignKey(People, on_delete=models.CASCADE)
   movie    = models.ForeignKey(Movie, on_delete=models.CASCADE)
   tmdb_id  = models.CharField(max_length=200)

   def __str__(self):
      return "ROLE" + self.role
