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


class moviedb:
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

   def find(self, filenameext):
      filename = self.clean(filenameext)
      data = self.moviedb.call(filename)
      year = m.gotyearintitle(filename)
      # Got 1 result
      if data["total_results"] == 1:
         return data["results"][0]
      # Got more result and got a date
      elif data["total_results"] >= 1 and year is not None:
         print " "
         print "_"*16
         print "Year of the film" + str(year)
         results = [result for result in data["results"] if result["release_date"][0:4] == year]
         print [r["title"] for r in results]
         print "_" * 16
         print " "
         sys.exit()
         pass
      # Des results mais pas de year
      elif data["total_results"] >= 1:
         print " "
         print "_"*16
         print [(result["title"]) for result in data["results"]]
         #compute levenshtein
         print "_"*16
         print " "

         #sys.exit()
      # 0 results but a year in the title
      elif year is not None:
         print "Year of the film" + str(year)
         filena = filename.split(year)
         for bits in filena:
            data = self.moviedb.call(bits)
            print data
            # Got 1 result
            if data["total_results"] == 1:
               return data["results"][0]
            elif data["total_results"] >= 1:
               resus = [result for result in data["results"] if result["release_date"][0:4] == year]
               if len(resus) > 0 and len(resus) < 4:
                  return resus[0]
            else:
               pass
         sys.exit()
         pass
      else:
         # weight = {}
         # for word in self.clean(filename).split(" "):
         #    w = self.mean.get(word)
         #    if w is not None:
         #       weight[word] = w
         #    else:
         #       data = moviedb.call(word)
         #       print " "
         #       print "*"*25
         #       print word
         #       print "-"*25
         #       print [(result["title"]) for result in data["results"]]
         #       print "*"*25
         #       print " "
         #       self.mean.add(word, data["total_results"])
         #       weight[word] = data["total_results"]
         # print weight

         # Combinaison 2 words
         pass


if __name__ == "__main__":
   files =  ["Mais.Qui.A.Tue.Pamela.Rose.avi",
            #"Love (2015) 720p VOST by Solon8 [MKV Corp].mkv",
            "Zach.Braff_2004_Garden.state.mkv",
            "Mais.qui.a.re-tue.Pamela.Rose.avi",
            "Colombiana (2011) 720p VO-VF by 4LT [MKV Corp].mkv",
            "La Colline aux coquelicots.avi",
            "Takeshi.Kitano_1989_Violent.Cop.mkv",
            "Bernard et Bianca au Pays dSes kangourous) (1990) 720p VO-VF by l'@rtiste [MKV Corp].mkv",
            "Blood Simple 1984 [Director's Cut].1984.DVDRip.XviD-VLiS.avi",
            "Dope (2015) 720p VOST by 4LT [MKV Corp].mkv"]
   m = moviedb()
   for i in files:
      m.find(i)
