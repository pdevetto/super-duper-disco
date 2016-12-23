from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Q
import hashlib, random, os, time, json
import utils
from library import movies

from .models import Movie, People, Role, Genre

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

def jsondata(request):
   response = {}

   response["total"] = Movie.objects.count()
   response["todo"] = Movie.objects.filter(clean=0).count()
   response["possible"] = Movie.objects.exclude(possible=0).count()

   return JsonResponse(response)

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

def possible(request):
   movie = request.GET.get('movie', False)
   possible = request.GET.get('tmdb', False)

   movieid = request.GET.get('movieid', False)
   search = request.GET.get('search', False)

   if movie and possible:
      elt = Movie.objects.get(pk=movie)
      #return HttpResponse(len(elt.possible))
      if json.loads(elt.possible) != 0:
         eltposs = [elt_possible for elt_possible in json.loads(elt.possible) if elt_possible['tmdb_id']==int(possible)]
         if len(eltposs) == 1:
            dat = eltposs[0]
            try:
               year = int(dat['year'][0:4])
            except :
               year = 0
            Movie.objects.filter(pk=elt.id).update(poster=dat['poster_path'], title=dat['title'], year=year, tmdb_id=dat['tmdb_id'], possible=0)
   if movieid and search:
      elt = Movie.objects.get(pk=movieid)
      #return HttpResponse(json.loads(elt.possible) != 0)
      if json.loads(elt.possible) != 0:
         Movie.objects.filter(pk=elt.id).update(search=search, possible=0)
   movies = Movie.objects.exclude(possible=0)
   movies_list = []
   for movie in movies:
      movie.possibles = json.loads(movie.possible)
      movies_list.append( movie )
   context = {'movies': movies_list}
   return render(request, 'possibles.htm', context)

def clear(request):
   Movie.objects.filter().delete()
   People.objects.filter().delete()
   Role.objects.filter().delete()
   Genre.objects.filter().delete()

   output = "All movies cleaned"
   return HttpResponse(output)

###########################
# Process LIBS
###########################

def processPeople(movie):
    ndata =0
    proc = movies.process()
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

       allpp = Role.objects.filter(role=peo["role"], movie=movie, people=people).count()

       if allpp == 0 and int(peo["role"]) <= 4 and int(peo["role"]) >=0:
          q = Role(role=peo["role"], movie=movie, people=people, tmdb_id=peo["cast_id"])
          q.save()
          ndata += 1
    return ndata

###########################
# Process
###########################

def btlog(txt, a, b):
   t = "<span style='border:1px solid black; padding:5px;'>"
   uu = int( (a - b)*1000 ) / 1000.0
   t += txt + str(uu) + "<br></span>"
   return ""
   #t

def process(request):
   formt = request.GET.get('format', 'html')
   delay = int(request.GET.get('delay', 4))
   start = time.time()
   response = {"log":"Processing merdiers", "nb":0}
   proc = movies.process()
   response["nb"] = 0
   movies_list = Movie.objects.filter(clean=0,possible=0)
   countmovie = len(movies_list)
   response["log"] += "<hr><hr>" + str(countmovie) + " movies to process"
   # process movie list
   for movie in movies_list:
      a = time.time()
      if int(time.time() - start ) >= delay:
         response["log"] += "<br>HTTP:" + str(proc.calls()) + "<hr> INTERUPTION :" + str( time.time() - start )
         break
      #################
      # For each movies
      response["log"] += "<br>HTTP:" + str(proc.calls()) + "<hr>" + movie.filename.encode("utf-8")
      response["log"] += "<br><i>" + str( int((time.time() - start  )*1000) /1000.0 ) + "</i>"
      proc.zero()
      if movie.tmdb_id != None and movie.tmdb_id != 0:
         response["log"] += "<br>***real actor"
         ##############################
         # That has no genres
         ndata = 0
         if movie.genres.count() == 0:
            response["log"] += "<br> -- genres:"
            dat = proc.genre(movie.tmdb_id)
            for g in dat:
                #response["log"] += ": " + str(g)
                if Genre.objects.filter(tmdb_id=g["id"]).count() == 0:
                    name = g["name"]
                    genre = Genre(name=name, tmdb_id=g["id"])
                    genre.save()
                else:
                    genre = Genre.objects.filter(tmdb_id=g["id"])[0]
                ndata += 1
                movie.genres.add(genre)
            if ndata == 0:
                if Genre.objects.filter(name="no").count() == 0:
                    genre = Genre(name="no", tmdb_id="0")
                    genre.save()
                    movie.genres.add(genre)
                    ndata += 1
                else:
                    genre = Genre.objects.filter(name="no")[0]
                    movie.genres.add(genre)
                    ndata += 1
            response["log"] += "" + str(ndata) + " genre !"
         ######################
         # That has no roles
         if Role.objects.filter(movie=movie.id).count() == 0:
            response["log"] += "<br> -- peoples:"
            ndata += processPeople(movie)
            response["log"] += str(ndata) + " added !"
         ######################
         # Process OK
         if ndata != 0:
            response["nb"] += 2
            Movie.objects.filter(pk=movie.id).update(clean=1)
      ################################
      # That does not exist
      elif movie.possible != 0:
         ################################
         # Specified search
         if movie.search != 0:
            response["log"] += "<br>*** manual:"
            dat = proc.find(movie.search)
         else:
            response["log"] += "<br>*** basic:"
            dat = proc.find(movie.filename)
         if dat == 0 or dat == None:
            Movie.objects.filter(pk=movie.id).update(possible=json.dumps([]))
            response["log"] += ">possible "
            response["nb"] += 1
         else:
             # Reponses multiples
             try:
                possibles = []
                for result in dat["possible"]:
                   possibles.append( {'poster_path':result['poster_path'], 'title':result['title'],
                   'original_title':result['original_title'], 'year':result['release_date'],'tmdb_id':result['id']} )
                Movie.objects.filter(pk=movie.id).update(possible=json.dumps(possibles))
                response["log"] += ">possible "
                response["nb"] += 1
             # Erreur
             except TypeError:
                return HttpResponse( str(dat) + "<br>" + movie.filename + "<br>" + str(dat) )
             # Reponse Simple
             except KeyError:
                try:
                   year = int(dat['release_date'][0:4])
                except :
                   year = 0
                try:
                   Movie.objects.filter(pk=movie.id).update( poster=dat['poster_path'], title=dat['title'], year=year, tmdb_id=dat['id'])
                   response["nb"] += 1
                   response["log"] += ">saved " + dat['title'].encode("utf-8")
                except TypeError:
                    pass

      # Add 'genre_ids'
      # Add 'original_title'
      # Add 'vote_average'
      # Add 'original_language'
      # Add the movie db 'id': 19898,

   end = time.time()
   response["time"] = end - start
   response["todo"] = Movie.objects.filter(clean=0).count()
   if formt == "json":
      return JsonResponse(response)
   else:
      return HttpResponse(response["log"])

def update(request):
   start = time.time()
   response = {"log":"Updating merdiers", "mov":[], "total":0, "nb":0}

   path = u"M:\Films"
   if not os.path.isdir(path):
      path = u"/media/data/Video/Movies/"
   if not os.path.isdir(path):
      path = u"/mnt/m/Films"
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
   response["todo"] = Movie.objects.filter(clean=0).count()
   end = time.time()
   response["time"] = end - start
   return JsonResponse(response)

def find(request, year=None, people=None, movie=None, genre=None):
    if movie != None:
        movie = Movie.objects.filter(id=movie)[0]
        peoples = Role.objects.filter(movie__id = movie.id)
        displays = [people.get_role_display() for people in peoples]
        context = {'movie': movie, 'peoples' :peoples, 'displays' : list(set(displays))}

        return render(request, 'movie.htm', context)
    context = {}
    if year != None:
        movies = Movie.objects.filter(year=year).distinct()
        context["findtype"] = "year"
    if people != None:
        movies = Movie.objects.filter(role__people__id=people).distinct()
        context["findtype"] = "people"
        context["people"] = People.objects.get(id=people)
    if genre != None:
        movies = Movie.objects.filter(genres__id=genre).distinct()
        context["findtype"] = "genre"

    movies_list = []
    for movie in movies:
        reals = People.objects.filter(role__movie__id = movie.id, role__role = 0)
        movies_list.append( (movie, reals) )
    context["movies_list"] = movies_list

    return render(request, 'movies.htm', context)
