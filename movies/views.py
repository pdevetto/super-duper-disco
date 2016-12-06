from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import hashlib, random, os, time
import utils
from library import movies

from .models import Movie, People, Role

def index(request):
    last = Movie.objects.count() - 1
    movies_list = []
    # Create a range of random index
    nrange = 24 if last > 24 else last-1
    idex = [random.randint(0, last) for a in range(nrange)]
    for indice in list(set(idex)):
       movie = Movie.objects.all()[indice]
       # get people with role of director for same movie id
       reals = People.objects.filter(role__movie__id = movie.id, role__role = 0)
       movies_list.append( (movie, reals) )
    context = {'movies_list': movies_list,}
    return render(request, 'movies.htm', context)

def isset(request):
   last = Movie.objects.exclude(year__isnull=True).count() - 1
   movies_list = []
   # Create a range of random index
   nrange = 30 if last > 30 else last-1
   idex = [random.randint(0, last) for a in range(nrange)]
   for indice in list(set(idex)):
     movie = Movie.objects.exclude(year__isnull=True)[indice]
     # get people with role of director for same movie id
     reals = People.objects.filter(role__movie__id = movie.id, role__role = 0)
     movies_list.append( (movie, reals) )
   context = {'movies_list': movies_list,'total':last}
   return render(request, 'movies.htm', context)


def clear(request):
   Movie.objects.filter().delete()
   People.objects.filter().delete()
   Role.objects.filter().delete()

   output = "All movies cleaned"
   return HttpResponse(output)

def process(request):
   start = time.time()
   response = {"log":"Processing merdiers", "nb":0}
   movies_list = Movie.objects.order_by('-title')
   proc = movies.process()
   response["nb"] = 0
   for movie in movies_list:
      if response["nb"] == 5:
          break
      # For each movies
      if movie.tmdb_id != None and movie.tmdb_id != 0:
         # That has no roles
         if Role.objects.filter(movie=movie.id).count() == 0:
            dat = proc.real(movie.tmdb_id)
            # FInd if people already exist
            for peo in dat:
               people = 0
               peoples = People.objects.filter(tmdb_id=peo["tmdb_id"])
               if len(peoples) == 0:
                  # create it
                  people = People(name=peo["name"], tmdb_id=peo["tmdb_id"], profile=peo["profile"])
                  people.save()
               else:
                  # retrieve it
                  people = peoples[0]

               allpp = Role.objects.filter(
                  role=peo["role"],movie=movie, people=people).count()

               if allpp == 0 and int(peo["role"]) <= 4 and int(peo["role"]) >=0:
                  q = Role(role=peo["role"], movie=movie, people=people, tmdb_id=peo["cast_id"])
                  q.save()
            response["nb"] += 1
      else:
         response["log"] += "<hr>" + movie.filename + " basic:"
         dat = proc.find(movie.filename)
         Movie.objects.filter(pk=movie.id)
         try:
             Movie.objects.filter(pk=movie.id).update(poster=dat['poster_path'], title=dat['title'], year=dat['release_date'][0:4], tmdb_id=dat['id'])
             response["nb"] += 1
         except TypeError:
             pass
         response["log"] += "<br>" + str(dat)

      # Add 'genre_ids'
      # Add reals :
      # Add 'original_title'
      # Add 'vote_average'
      # Add 'original_language'
      # Add the movie db 'id': 19898,

   end = time.time()
   response["time"] = end - start
   return JsonResponse(response)

def update(request):
   start = time.time()
   response = {"log":"Updating merdiers", "mov":[], "total":0, "nb":0}

   path = u"M:\Films"
   if not os.path.isdir(path):
      path = u"/media/data/Video/Movies/"
   for movie in utils.parse(path):
      if response["nb"] == 40:
         break
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
   end = time.time()
   response["time"] = end - start
   return JsonResponse(response)

def find(request, year=None, director=None, movie=None):
   if year != None:
      movies = Movie.objects.filter(year=year)
   if director != None:
      movies = Movie.objects.filter(role__people__id=director, role__role = 0)
   if movie != None:
      movies = Movie.objects.filter(id=movie)

   movies_list = []
   for movie in movies:
      reals = People.objects.filter(role__movie__id = movie.id, role__role = 0)
      movies_list.append( (movie, reals) )
   context = {'movies_list': movies_list,}
   return render(request, 'movies.htm', context)
