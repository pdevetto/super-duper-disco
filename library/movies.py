import ConfigParser, requests, os, sys, re, json

class moviedbapi:
   def __init__(self):
      config = ConfigParser.ConfigParser()
      current = os.path.dirname(os.path.realpath(__file__))
      config.read(os.path.join(current, "config.ini"))
      self.key = config.get("themoviedb",'apikey')

   def call(self, query):
      url = "https://api.themoviedb.org/3/search/movie"
      params = {'api_key':self.key, "query" : query, 'language' : 'fr'}
      headers = { 'Accept': 'application/json' }
      r = requests.get(url, params=params, headers=headers)
      return r.json()

   def movie(self, movie_id):
      url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + ""
      params = {'api_key':self.key, 'language' : 'fr'}
      headers = { 'Accept': 'application/json' }
      r = requests.get(url, params=params, headers=headers)
      return r.json()


   def peoples(self, movie_id):
      url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/credits"
      params = {'api_key':self.key, 'language' : 'fr'}
      headers = { 'Accept': 'application/json' }
      r = requests.get(url, params=params, headers=headers)
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


class process:
   # ['vo', 'vostfr', 'dvdrip', 'brrip', '720p', '1080p', 'wawa', 'xvid', 'www']

   def __init__(self):
      self.moviedb = moviedbapi()
      self.mean = meanwords()

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
      if len(years) == 1:
         return years[0]

   def genre(self, movie_id):
       dat = self.moviedb.movie(movie_id)
       return dat["genres"]

   def find(self, filenameext):
      filename = self.clean(filenameext)
      data = self.moviedb.call(filename)
      year = self.gotyearintitle(filename)
      # Got 1 result
      if data["total_results"] == 1:
         return data["results"][0]
      # Got more result and got a date
      elif data["total_results"] >= 1 and year is not None:
         results = [result for result in data["results"] if result["release_date"][0:4] == year]
         pass
      # Des results mais pas de year
      elif data["total_results"] >= 1:
         #compute levenshtein
         pass
         #sys.exit()
      # 0 results but a year in the title
      elif year is not None:
         filena = filename.split(year)
         for bits in filena:
            data = self.moviedb.call(bits)
            # Got 1 result
            if data["total_results"] == 1:
               return data["results"][0]
            elif data["total_results"] >= 1:
               resus = [result for result in data["results"] if result["release_date"][0:4] == year]
               if len(resus) > 0 and len(resus) < 4:
                  return resus[0]
            else:
               pass
         pass
      else:
         # Combinaison 2 words
         pass
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
   # files =  ["Mais.Qui.A.Tue.Pamela.Rose.avi",
   #          #"Love (2015) 720p VOST by Solon8 [MKV Corp].mkv",
   #          "Zach.Braff_2004_Garden.state.mkv",
   #          "Mais.qui.a.re-tue.Pamela.Rose.avi",
   #          "Colombiana (2011) 720p VO-VF by 4LT [MKV Corp].mkv",
   #          "La Colline aux coquelicots.avi",
   #          "Takeshi.Kitano_1989_Violent.Cop.mkv",
   #          "Bernard et Bianca au Pays dSes kangourous) (1990) 720p VO-VF by l'@rtiste [MKV Corp].mkv",
   #          "Blood Simple 1984 [Director's Cut].1984.DVDRip.XviD-VLiS.avi",
   #          "Dope (2015) 720p VOST by 4LT [MKV Corp].mkv"]
   m = process()
   # for i in files:
   #    m.find(i)
   movieids = [292431, 12622, 308639, 62835, 401, 139374]
   for i in movieids:
       m.genre(i)
