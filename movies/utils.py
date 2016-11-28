import os, sys

def parse(path):
   for m_file in os.listdir(path):
      current = os.path.join(path, m_file)
      if not os.path.isfile(current):
         parse(current)
      else:
         filext = os.path.splitext(current)[1]
         if filext in [".mkv", ".avi"]:
            yield [path, m_file]
         else:
            print filext


if __name__ == "__main__":
   #open_browser()
   for machin in parse("/media/data/Video/Movies"):
      print "  - " + machin[1]
