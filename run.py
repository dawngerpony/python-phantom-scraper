############################################################################################
from   bs4 import BeautifulSoup
import multiprocessing
import os
import pickle
import requests
from   subprocess import call
import sys
import tempfile

globallock = multiprocessing.Lock()

def run(url, cssClass):
    """ Runs the check() job <total> times and keeps track of how many times the
        job was successful.
    """
    total = 10
    jobs = []
    counter = "counter.pickle"
    with open(counter, "w") as f:
        pickle.dump(0, f)
    for i in range(1,total):
        p = multiprocessing.Process(target=check, args=(i, url, cssClass))
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()
    numNew = 0
    with open(counter) as f:
        numNew = pickle.load(f)
    os.remove(counter)
    print "New: %d, old: %d = %.2f%%" % (numNew, total-numNew, ((float(numNew)/float(total))*100.0))
    percentage = (float(numNew)/float(total))*100.0

def check(i, url, cssClass):
    """ Checks the contents of a web page for a specific CSS class.
        Downloads the file using PhantomJS because we need to execute the JavaScript.
        Increments a global file-based counter for each time the class is found at least once
        in the web page.
    """
    print "Job %d" % i
    with tempfile.NamedTemporaryFile(prefix="out_", suffix=".html", dir=".") as outfile:
        call(["./phantomjs", "savepage.js", url, outfile.name])
        with open(outfile.name, "r") as f:
            soup = BeautifulSoup(f)
            mydivs = soup.findAll("div", { "class" : cssClass })
            if len(mydivs) > 0:
                print "NEW!"
                increment()
            else:
                print "OLD"

def increment():
    """ Increment a counter stored in a file.
    """
    globallock.acquire()
    i = 0
    counter = "counter.pickle"
    if os.path.isfile(counter):
        with open(counter) as f:
            i = pickle.load(f)
            i += 1
    with open(counter, "w") as f:
        pickle.dump(i, f)
    globallock.release()

if __name__ == "__main__":
    url = sys.argv[1]
    cssClass = sys.argv[2]
    run(url, cssClass)
