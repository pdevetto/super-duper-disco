import ConfigParser, requests, os, sys, re, json, Levenshtein, time, pprint

class moviedbapi:
   def __init__(self):
      config = ConfigParser.ConfigParser()
      current = os.path.dirname(os.path.realpath(__file__))
      config.read(os.path.join(current, "config.ini"))
      self.key = config.get("themoviedb",'apikey')
      self.httpcalls = 0

   def call(self, query):
      url = "https://api.themoviedb.org/3/search/movie"
      params = {'api_key':self.key, "query" : query, 'language' : 'fr'}
      headers = { 'Accept': 'application/json' }
      r = requests.get(url, params=params, headers=headers)
      self.httpcalls += 1
      return r.json()

   def movie(self, movie_id):
      url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + ""
      params = {'api_key':self.key, 'language' : 'fr'}
      headers = { 'Accept': 'application/json' }
      r = requests.get(url, params=params, headers=headers)
      self.httpcalls += 1
      return r.json()


   def peoples(self, movie_id):
      url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/credits"
      params = {'api_key':self.key, 'language' : 'fr'}
      headers = { 'Accept': 'application/json' }
      r = requests.get(url, params=params, headers=headers)
      self.httpcalls += 1
      return r.json()

class meanwords:
   def __init__(self):
      basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
      self.wordfile = os.path.join(basepath, 'meanwords.json')
      self.base = self.load()
      if self.base is None:
         self.base = {}

   def get(self, word):
      try:
         return self.base[word]
      except KeyError:
         return None

   def save(self):
      with open(self.wordfile, 'w+') as f:
         json.dump(self.base, f)

   def load(self):
      try:
         with open(self.wordfile, 'r') as f:
            data = json.load(f)
      except IOError:
         return {}
      except ValueError:
         return {}

   def add(self, word, value):
      self.base[word] = value
      self.save()

# Reading data back
def btlog(txt, a, b):
   t = "<br><span style='border:1px solid black; padding:5px;'>"
   uu = int( (a - b)*1000 ) / 1000.0
   t += txt + str(uu) + "<br></span>"
   return ""
   #return t

class process:
   # ['vo', 'vostfr', 'dvdrip', 'brrip', '720p', '1080p', 'wawa', 'xvid', 'www']

   def __init__(self):
      self.moviedb = moviedbapi()
      self.mean = meanwords()

   def zero(self):
      self.moviedb.httpcalls = 0
   def calls(self):
      return self.moviedb.httpcalls

   def clean(self, filename):
      """
      Remove extension and replace punctuation by spaces
      """
      spli = os.path.splitext(filename)
      filename = spli[0]
      filename = filename.replace(".", " ").replace("_", " ").replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ").replace("  ", " ")
      return filename

   def subsets(self, filename):
      """
      Test different subsets of words in order to detect which words are usefull
      """
      pass

   def format(self, result):
      return result
      #{'poster_path','title','overview','release_date','original_title','vote_count': 26,'vote_average': 5.5,'original_language': u'fr','id': 139374,'genre_ids': [35]}]}
      #results_year = [x for x in results if x['year'] != "" and x['year'] in req]

   def gotyearintitle(self, filename):
      years = re.findall("(?:[^0-9]|^)((?:19|20)[0-9][0-9])(?:[^0-9]|$)", filename)
      years = list(set(years))
      if len(years) == 1:
         return years[0]

   def genre(self, movie_id):
       dat = self.moviedb.movie(movie_id)
       return dat["genres"]

   def levendata(self, bitsdata, tresh=0.1):
      if bitsdata == []:
         return None
      min_leven = 10000
      result_leven = None
      results_leven = []
      coun = 0
      to = 0
      for bits, result in bitsdata:
         distance = Levenshtein.distance(bits.decode("utf-8"), result["title"])
         if distance == min_leven:
            coun += 1
            results_leven.append( result )
         if distance < min_leven:
            min_leven = distance
            result_leven = result
            results_leven = [result]
            coun = 0
            to = min_leven / len(bits)
      print " " * 10 + "-- LEVENSHTEIN * " + str(coun) + " AT " + str(min_leven) + " to: " + str(to) + " : " + result_leven["title"].encode("utf-8")
      if coun == 0:
         if to <= tresh:
            return result_leven
         else:
            return None
      else:
         return {"possible":results_leven}


   def find(self, filenameext):
      log = ""
      a = time.time()
      filename = self.clean(filenameext)
      b = time.time()
      print " " * 4 + "-- " + filename.decode("utf-8")
      data = self.moviedb.call(filename)
      c = time.time()
      year = self.gotyearintitle(filename)
      d = time.time()
      log += btlog("clean",  b, a)
      log += btlog("movidb", c, b)
      log += btlog("gotyear", d, c)
      # Got 1 result
      if data["total_results"] == 1:
         print " " * 8 + "-- 1 result"
         return data["results"][0], log
      # Got more results and got a date
      elif data["total_results"] >= 1 and year is not None:
         d = time.time()
         print " " * 8 + "-- * results - 1 year"
         results = [result for result in data["results"] if result["release_date"][0:4] == year]
         e = time.time()
         log += btlog("comprehension",  e, d)
         if len(results) == 1:
            return results[0], log
         else:
            return {"possible":results}, log
      # Des results mais pas de year
      elif data["total_results"] >= 1:
         e = time.time()
         print " " * 8 + "-- * results - no year"
         bitsdata = [(filename, result) for result in data["results"]]
         f = time.time()
         res = self.levendata(bitsdata, tresh=0.3)
         g = time.time()
         log += btlog("bitsdata",  f, e)
         log += btlog("levendata",  g, f)
         if res != None:
            try:
               return res["possible"], log
            except:
               return res, log
         else:
            return {"possible": data["results"]}, log
         #sys.exit()
      # 0 results but a year in the title
      elif year is not None:
         print " " * 8 + "-- 0 result - year"
         filena = filename.split(year)
         databits = {}
         for bits in filena:
            a = time.time()
            data = self.moviedb.call(bits)
            b = time.time()
            databits[bits] = data
            print " " * 8 + ">- " + bits + " = " + str(data["total_results"]) + " results"
            # Got 1 result for petit title
            c = time.time()
            log += btlog("dbcall sous ",  b, a)
            log += btlog("giberish",  c, b)
            if data["total_results"] == 1:
               return data["results"][0], log
            # got more results
            elif data["total_results"] >= 1:
               # Try if year break the results
               resus = [result for result in data["results"] if result["release_date"][0:4] == year]
               if len(resus) == 1:
                  return resus[0], log
         # levenshtein on results with half bits
         bitsdata = [(bits, result) for bits, data in databits.items() for result in data["results"] ]

         b = time.time()
         res = self.levendata(bitsdata, tresh=0.3)
         c = time.time()
         log += btlog("2 leven ",  c, b)
         if res != None:
            return res, log
         else:
            return {"possible": [result for (bits, result) in bitsdata]}, log

         # for bits, data in databits.items():
         #    bits = bits.strip()
         #    for result in data["results"]:
         #       distance = Levenshtein.distance(bits.decode("utf-8"), result["title"])
         #       if distance == min_leven:
         #          coun += 1
         #       if distance < min_leven:
         #          min_leven = distance
         #          result_leven = result
         #          coun = 0
         # print " " * 10 + "-- LEVENSHTEIN * " + str(coun) + " AT " + str(min_leven) + " len(bits) " + str(len(bits))
         # if min_leven / len(bits) <= 0.3 and coun == 0:
         #    return result_leven
         # else:
         #    return {"possible": [result for result in data["results"] for data in databits]}
      else:
         print " " * 8 + "-- 0 result"
         # Combinaison 2 words

   def real(self, movie_id):
      #print "REAL" + str(movie_id)
      dat = self.moviedb.peoples(movie_id)
      peoples = []
      for cast in dat["cast"]:
         peoples.append({ "name" : cast["name"], "tmdb_id" : cast["id"], "profile" : cast["profile_path"], "role" : 1, "cast_id": cast["cast_id"]})
         #print cast
      for cast in dat["crew"]:
         roles = {
            "Directing":0,
            "Director":0,
            "Producer":2,
            "Executive Producer":2,
            "Screenplay":3,
            "Adaptation":3,
            "Director of Photography":4,
            "Writing":5,
            "Writer":5,
         }
         try:
            #print cast
            role = roles[cast["job"]]
            if role != -1:
               peoples.append( { "name" : cast["name"], "tmdb_id" : cast["id"], "profile" : cast["profile_path"], "role" : role, "cast_id": cast["credit_id"]} )
         except KeyError:
            pass
            #print "NEW LABEL : " + cast["job"]

      return peoples

if __name__ == "__main__":
   files =  ["Dope (2015) 720p VOST by 4LT [MKV Corp].mkv",
            #"Ne.le.dis.a.personne.CD1.avi",
            #  "Fabien Onteniente 2009 Camping 2",
            #  "Love (2015) 720p VOST by Solon8 [MKV Corp].mkv",
            # "Zach.Braff_2004_Garden.state.mkv",
            #  "Mais.qui.a.re-tue.Pamela.Rose.avi",
            #  "Colombiana (2011) 720p VO-VF by 4LT [MKV Corp].mkv",
            #  "La Colline aux coquelicots.avi",
            #  "Takeshi.Kitano_1989_Violent.Cop.mkv",
            #  "Bernard et Bianca au Pays dSes kangourous) (1990) 720p VO-VF by l'@rtiste [MKV Corp].mkv",
            #  "Blood Simple 1984 [Director's Cut].1984.DVDRip.XviD-VLiS.avi",
            #  "Dope (2015) 720p VOST by 4LT [MKV Corp].mkv"
            ]
   m = process()
   for i in files:
       r, log = m.find(i)
       if r is not None:
          try:
             a = r["possible"]
             print "**possibles**"
          except:
             print r
             print "**saved**"

   #movieids = [292431, 12622, 308639, 62835, 401, 139374]
   #for i in movieids:
   #    m.genre(i)
