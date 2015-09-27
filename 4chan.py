import urllib2
import json
import argparse
import re
import os

validURL = r"http[s]?:\/\/boards\.4chan\.org\/(\w+)\/thread\/(\d+)" # board, thread
jsonURL  = "https://a.4cdn.org/%s/thread/%s.json"                   # board, thread
imageURL = "https://i.4cdn.org/%s/%s%s"                             # board, file, extension


def argParser():
    parser = argparse.ArgumentParser(description='Image downloader for 4chan version 2')
    parser.add_argument('input', nargs='?', help='HTML link to a 4chan thread')
    parser.add_argument('-d', '--path', help='The destination folder',
                        required=False)
    return parser.parse_args()


def getURLFromClipboard():
    from Tkinter import Tk
    r = Tk()
    r.withdraw()
    url = r.clipboard_get()
    r.destroy
    print "Copied URL from clipboard"
    return url


def getMatchesFromURL(url):
    match = re.search(validURL, url)
    if not match:
        print "URL Error: URL is not a 4chan thread URL!"
        exit(1)
    return (match.group(1), match.group(2)) # board, thread


def fetchJSON(url, board, thread):
    try:
        response = urllib2.urlopen(jsonURL % (board, thread))
        return response.read()
    except(ValueError, urllib2.URLError, urllib2.URLError) as e:
        print e
        exit(1)        


def downloadImages(data, board):
    if not os.path.exists(path):
        os.makedirs(path)
    print "Downloading to %s" % path
    print "Images found: %d" % (data["posts"][0]["images"] + 1)
    for post in data["posts"]:
        if "tim" in post:
            tim, ext = (post["tim"], post["ext"]) # time = filename
            image = imageURL % (board, tim, ext)
            saveImage(image, "%s%s" % (tim, ext))


def saveImage(image, filename):
    global imageCount
    imagepath = os.path.join(path, filename)
    if not os.path.isfile(imagepath):
        f = urllib2.urlopen(image)
        with open(os.path.abspath(imagepath), "wb") as local_file:
            print "-> %s" % filename
            local_file.write(f.read())
            imageCount += 1


def main():
    global path
    global imageCount

    imageCount = 0
    args = argParser()                                      # Get input
    url = args.input or getURLFromClipboard()               # Get url
    board, thread = getMatchesFromURL(url)                  # Get board and thread
    path = args.path or "4chan_Images"                      # Set path
    path += "\\%s_%s" % (board, thread)                     # Add image folder to path

    data = json.loads(fetchJSON(url, board, thread))        # Get JSON data
    downloadImages(data, board)                             # Download images
    print "Images added: %d" % imageCount

if __name__ == "__main__":
    main()
