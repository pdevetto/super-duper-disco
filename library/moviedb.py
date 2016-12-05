import ConfigParser, requests, os, sys, re

class moviedbapi:
   def __init__(self):
      config = ConfigParser.ConfigParser()
      current = os.path.dirname(os.path.realpath(__file__))
      config.read(os.path.join(current, "config.ini"))
      self.key = config.get("themoviedb",'apikey')

   def call(self, query, pref):
      print pref + "call"
      url = "https://api.themoviedb.org/3/search/movie"
      params = {'api_key':self.key, "query" : query, 'language' : 'fr'}
      headers = { 'Accept': 'application/json' }
      r = requests.get(url, params=params, headers=headers)
      return r.json()

class moviedb:
   # ['vo', 'vostfr', 'dvdrip', 'brrip', '720p', '1080p', 'wawa', 'xvid', 'www']

   def clean(self, filename):
      """
      Remove extension and replace punctuation by spaces
      """
      print 4*" " + "clean:"
      spli = os.path.splitext(filename)
      filename = spli[0]
      filename = filename.replace(".", " ").replace("_", " ").replace("  ", " ")
      print 8*" " + filename
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

   def gotyearintitle(filename):
      match = re.match(r'.*([19-20][0-9]{2})', l)
      print match
      sys.exit()
      if match is not None:
         print match.group(1)


   def find(self, filename):
      moviedb = moviedbapi()
      print filename
      data = moviedb.call(filename, 4*" ")
      print 4*" " + str(data)
      if data["total_results"] == 1:
         print "--{ " + data["results"] + " }"
         return data["results"][0]
      if data["total_results"] == 0:
         data = moviedb.call(self.clean(filename), 8*" ")
         print 8*" " + str(data)
         if data["total_results"] == 1:
            ## SELECT ONE
            print "--{ " + data["results"] + " }"
            return data["results"][0]
         elif data["total_results"] >= 1:
            ## SELECT ONE
         elif data["total_results"] == 0:
            data = moviedb.call(self.filter(self.clean(filename)), 16*" ")


if __name__ == "__main__":
   files =  ["Mais.Qui.A.Tue.Pamela.Rose.avi",
            "Love (2015) 720p VOST by Solon8 [MKV Corp].mkv",
            "Zach.Braff_2004_Garden.state.mkv",
            "Mais.qui.a.re-tue.Pamela.Rose.avi",
            "Colombiana (2011) 720p VO-VF by 4LT [MKV Corp].mkv",
            "La Colline aux coquelicots.avi",
            "Takeshi.Kitano_1989_Violent.Cop.mkv",
            "Bernard et Bianca au Pays des kangourous) (1990) 720p VO-VF by l'@rtiste [MKV Corp].mkv",
            "Blood Simple 1984 [Director's Cut].1984.DVDRip.XviD-VLiS.avi",
            "Dope (2015) 720p VOST by 4LT [MKV Corp].mkv"]
   m = moviedb()
   m.gotyearintitle("as 2012 qdqs 1099")
   m.gotyearintitle("as 2200 qdqs")
   for i in files:
      m.find(i)
