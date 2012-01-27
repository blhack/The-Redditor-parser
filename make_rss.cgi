#!/usr/bin/python

import urllib
import feedparser
from BeautifulSoup import BeautifulSoup
import urlparse


def fetch_feed(url):
	req = urllib.urlopen(url)
	data = req.read()
	return(data)

def parse_xml(data):
	xml = feedparser.parse(data)
	return(xml)

def walk_xml(xml):
	entries = []
	for entry in xml['entries']:
		title = entry['title']
		description = entry['summary_detail']['value']
		entries.append([title,description])
	return(entries)

def find_tiny_url(entry):
	soup = BeautifulSoup(entry)
	pdf = ""
	for link in soup.findAll('a'):
		link = str(link['href'])
		url = urlparse.urlparse(link)
		if url[1] == "tinyurl.com":
			pdf = link

	return(pdf)

if __name__ == "__main__":

	#first, set up an XML header

	print "content-type:application/rss+xml"
	print

	print "<?xml version='1.0' encoding='ISO-8859-1'?>"
	print "<rss version='2.0'>"
	print "<channel>"
	print """
	<title>PDFs of The Redditor</title>
	<link>http://theredditor.com</link>
	<description>A Magazine about Reddit</description>
	"""

	data = fetch_feed("http://theredditorissues.blogspot.com/feeds/posts/default?alt=rss")
	xml = parse_xml(data)
	walk_xml(xml)
	entries = walk_xml(xml)
	for entry in entries:
		title = entry[0]
		description = entry[1]
		tiny_url = find_tiny_url(description)
		if len(tiny_url) > 0:
			print "<item>"
			print "<title>"
			print title
			print "</title>"
			print "<link>"
			print tiny_url
			print "</link>"
			print "</item>"
	print "</channel>"
	print "</rss>"
