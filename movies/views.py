from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import hashlib, random
import utils
from library import movies

from .models import Movie

def index(request):
    #movies_list = Movie.objects.order_by('-title')
    movies_list = []
    last = Movie.objects.count() - 1
    nrange = 24 if last > 24 else last-1
    idex = [random.randint(0, last) for a in range(nrange)]
    for indice in list(set(idex)):
        movies_list.append( Movie.objects.all()[indice] )
    context = {'movies_list': movies_list,}
    return render(request, 'movies.htm', context)

def clear(request):
   Movie.objects.filter().delete()
   output = "All movies cleaned"
   return HttpResponse(output)

def process(request):
   movies_list = Movie.objects.order_by('-title')
   response = ""
   proc = movies.process()
   processed = 0
   for movie in movies_list:
      if processed == 20:
          break
      processed += 1
      response += "<hr>" + movie.filename + ":"
      dat = proc.find(movie.filename)
      response += "<br>" + str(dat)
   return HttpResponse(response)

def update(request):
   response = {"log":"Updating merdiers", "mov":[], "total":0, "nb":0}

   path = u"M:\Films"
   for movie in utils.parse(path):
      hust = hashlib.sha224(movie[1].encode("utf-8")).hexdigest()
      count = Movie.objects.filter(titlehash=hust).count()
      response["log"] += "\n / " + str(count) + " movies in database + " + str(hust)
      response["total"] += 1
      if count == 0:
         response["nb"] += 1
         response["mov"].append(movie[1])
         q = Movie(titlehash=hust, filename=movie[1], filepath=movie[0])
         q.save()
   response["log"] = ""
   return JsonResponse(response)

def movie(request, movie_id):
   response = "You're looking at movie %s."
   return HttpResponse(response % movie_id)
