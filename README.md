4chan image downloader Version 2
======================

####Requires python 2.7####

:tada: **New**: Now uses JSON instead of Regex to retrieve image links!

Code has been cleaned up, making it more modular and easier to read.

Usage:
```sh
$ python 4chan.py https://boards.4chan.org/g/thread/123456789
```

It can also copy the URL from your clipboard, given that the URL is a correct:

```sh
$ python 4chan.py
```

Add a custom path by adding `-d path` (Does not need to contain the URL):

```sh
$ python 4chan.py [url] -d C:\\Some\Path\Example
```
