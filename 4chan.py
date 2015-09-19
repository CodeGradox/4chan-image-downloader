from urllib2 import urlopen
from sys import exit
import re
import argparse
import os


def validURL(s):
    from urlparse import urlparse
    o = urlparse(s)
    if o.scheme == 'http' or 'https':
        return True
    return False


def getURLfromClipboard():
    from Tkinter import Tk
    r = Tk()
    r.withdraw()
    s = r.clipboard_get()
    r.destroy
    if not validURL(s):
        print 'Invalid URL'
        exit(1)
    print ' Copied URL from clipboard'
    return s

parser = argparse.ArgumentParser(description='Image downloader for 4chan')
parser.add_argument('input', nargs='?', help='HTML link to a thread on 4chan',
                    default=getURLfromClipboard())
parser.add_argument('-d', '--destination', help='The destination folder',
                    required=False)

args = parser.parse_args()

url = args.input
destination = args.destination if args.destination else '4chan_Images/'

try:
    html = urlopen(url).read()
except ValueError:
    print ' Invalid url or thread is 404'
    exit(1)

tmp = re.search(r'([a-zA-Z]+)/thread/(\d+)/?', url)
board = tmp.group(1)
thread = tmp.group(2)

destination += board + '_' + thread + '/'

pat = r'<a class=\"[\w -]+\" href="(//i.4cdn.org/[a-zA-Z]+/(\d+.[a-zA-Z]+))"'
links = re.findall(pat, html)

if not os.path.exists(destination):
    os.makedirs(destination)

print ' Downloading to %s' % destination
print ' %d images found' % len(links)

counter = 0
for link in links:
    path = os.path.join(destination, link[1])

    if not os.path.isfile(path):
        f = urlopen('http:' + link[0])
        with open(os.path.abspath(path), 'wb') as local_file:
            print 'Downloading %s' % link[1]
            local_file.write(f.read())
            counter += 1
print ' %d new images added' % counter
