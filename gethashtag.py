# -*- coding: utf-8  -*-
import argparse
import urllib
import urllib2
import json
import re

TWITTER_API  = "http://search.twitter.com/search.json?q="
TWITTER_ID   = "https://twitter.com/{user}/status/{id}"

def getArgs():
    """Parse command-line arguments with optional functionalities"""
    
    parser = argparse.ArgumentParser(description='Retrieve unique URLs found in the most recent tweets on Twitter')
    parser.add_argument('hashtag')
    parser.add_argument('-t','--tweets', dest="tweets", type=int, default=100, metavar="number_of_tweets", help="Number of tweets to retrieve (defaults to 100)")
    parser.add_argument('-u','--url', action="store_true", dest="url", help="Print the URL of the tweet page which includes inner URL")
    
    result = parser.parse_args()
    if result.tweets <= 0:
        msg = "Number of tweets cannot be smaller than 1."
        raise argparse.ArgumentTypeError(msg)
    
    return result.hashtag, result.tweets, result.url


def getJSON(hashtag, tweets, url=False):
    """Get JSON source text in string format"""
    
    if hashtag.startswith("#"):
        hashtag = hashtag[1:]
    hashtag = urllib.quote(hashtag)
    print hashtag
    f = None
    try:
        api_url = TWITTER_API + '%23' + hashtag + '&rpp=' + str(tweets)
        #print api_url
        f = urllib2.urlopen(api_url)
    except:
        raise
    return f

def parseJSON(f):
    results = json.load(f)['results']
    urls = []
    for result in results:
        url = matchShortURL(result['text'])
        if url:
            id = result['id_str']
            user = result['from_user']
            t_url = TWITTER_ID.format(id=id, user=user)
            urls.append((url, t_url))
    return urls
                
def matchShortURL(text):
    """Match http://t.co/fooBar in text"""
    pattern = 'http://t.co/[a-zA-z0-9]{8}'
    r = re.search(pattern, text)
    if r:
        url = r.group()
        return url
    else:
        return None

def main():
    h, t, u = getArgs()
    json = getJSON(h, t, u)
    urls = parseJSON(json)
    d = dict(urls).items()
    if u:
        for url in d:
            print url[0] + " @ " + url[1]     
    else:
        for url in d:
            print url[0]    
    
if __name__ == '__main__':
    main()