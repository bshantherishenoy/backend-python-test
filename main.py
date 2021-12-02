"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
import subprocess


from alayatodo import app



if __name__ == '__main__':
    print("Came here")
    args = docopt(__doc__)
    if args['initdb']:

        print("AlayaTodo: Database initialized.")
    else:
        print("AlayaTodo: Database initialized.")
        app.run(use_reloader=True)
