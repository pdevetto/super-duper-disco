from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

def index(request):
   output = "Hello, world. All the movies."
   movies = Movie.objects.order_by('-title_hash')
   output += ', '.join([m for m in movies])
   return HttpResponse(output)

def update(request):
   response = "Updating merdiers"

   q = Movie(title="What's new?", pub_date=timezone.now())
   q.save()

   title      = models.CharField(max_length=200, blank=True)
   title_hash = models.CharField(max_length=200, blank=True)
   filename   = models.CharField(max_length=200, blank=True)
   year       = models.DateTimeField('Movie year')
   director

   return HttpResponse(response)

def movie(request, movie_id):
   response = "You're looking at movie %s."
   return HttpResponse(response % movie_id)
