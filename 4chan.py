from urllib2 import urlopen
from urllib2 import URLError
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
parser.add_argument('input', nargs='?', help='HTML link to a thread on 4chan')
parser.add_argument('-d', '--destination', help='The destination folder',
                    required=False)

# Check arguments
args = parser.parse_args()

# Get url from args or clipboard and setup download path
url = args.input if args.input else getURLfromClipboard()
destination = args.destination + '\\' if args.destination else '4chan_Images/'

# Get the thread
try:
    html = urlopen(url).read()
except ValueError:
    print ' Invalid URL or thread is 404'
    exit(1)
except URLError, e:
	print ' Invalid or broken URL'
	exit(1)

# Get the thread number and board name
tmp = re.search(r'([a-zA-Z]+)/thread/(\d+)/?', url)
board = tmp.group(1)
thread = tmp.group(2)

# Append destination folder to download path
destination += board + '_' + thread + '/'

# Create destination folder
if not os.path.exists(destination):
    os.makedirs(destination)

# Regex for finding the img tags from the HTML document
pat = r'<a class=\"[\w -]+\" href="(//i.4cdn.org/[a-zA-Z]+/(\d+.[a-zA-Z]+))"'
links = re.findall(pat, html)

print ' Downloading to %s' % destination
print ' %d images found' % len(links)

# Download all the images to destination folder
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
