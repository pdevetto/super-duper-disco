from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import hashlib
import utils
import library.moviedb


from .models import Movie

def index(request):
   movies_list = Movie.objects.order_by('-title')
   context = {'movies_list': movies_list,}
   return render(request, 'movies.htm', context)

def clear(request):
   Movie.objects.filter().delete()
   output = "All movies cleaned"
   return HttpResponse(output)

def process(request):
   movies_list = Movie.objects.order_by('-title')
   response = ""
   #m = moviedb()
   for movie in movies_list:
      response += "<hr>" + movie.filename + ":"
      #response += "<br>" + str(m.find(movie.filename))
   return HttpResponse(response)

def update(request):
   response = {"log":"Updating merdiers", "mov":[], "total":0, "nb":0}

   path = "/media/data/Video/Movies"
   for movie in utils.parse(path):
      hust = hashlib.sha224(movie[1]).hexdigest()
      count = Movie.objects.filter(titlehash=hust).count()
      response["log"] += "\n / " + str(count) + " movies in database + " + str(hust)
      response["total"] += 1
      if count == 0:
         response["nb"] += 1
         response["mov"].append(movie[1])
         q = Movie(titlehash=hust, filename=movie[1], filepath=movie[0])
         q.save()
   return JsonResponse(response)

def movie(request, movie_id):
   response = "You're looking at movie %s."
   return HttpResponse(response % movie_id)
