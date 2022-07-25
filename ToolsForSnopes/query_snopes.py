from bs4 import BeautifulSoup as bs
import sys
from bs4 import SoupStrainer as ss
import requests
from urllib.parse import urlencode
import string
import codecs

# Function to generate encoded query url from a string
def generate_query_url(snopes_query):
    query_dict = {'s': snopes_query}
    return ('https://www.snopes.com/?' + urlencode(query_dict))

# Function to grab all links from a query url that are fact checks
def grab_links(query_url):
    # Make request, setup bs object
    only_links = ss('a', class_="link")
    html = requests.get(query_url)
    html_text = html.text
    soup = bs(html_text, "html.parser", parse_only=only_links)
    # Create list with links to all fact check articles found
    list_of_links = []
    fact_check_url = 'https://www.snopes.com/fact-check/'
    for link in soup.find_all('a'):
        url = link.get('href')
        if url[:34] == fact_check_url:
            list_of_links.append(url)
    
    return list_of_links

# Given a url for a fact check article, returns the truth rating from it
def grab_rating(article_url):
    # Make request, setup bs object
    rating_strainer = ss(class_ = ['figure-image img-responsive img-fluid w-100 Media--image', 'figure-image img-responsive img-fluid w-100'])
    html = requests.get(article_url)
    html_text = html.text
    soup = bs(html_text, 'html.parser', parse_only = rating_strainer)
    # Grab and return the truth rating from the article
    tag = soup.img
    return tag.get('alt')

def generate_snopes_query(tweet_text):
    if len(tweet_text) < 99:
        snopes_query = tweet_text
    else:
        snopes_query = tweet_text[:99]
        if tweet_text[99] not in string.whitespace:
            index = snopes_query.rfind(" ")
            snopes_query = snopes_query[:index]
    print(snopes_query)
    return generate_query_url(snopes_query)

def main(argv):
    if(len(sys.argv) != 2):
        print("Incorrect number of arguments; please provide only path to input file")
    # Open input file
    try:
        f = codecs.open(sys.argv[1], 'r', 'utf-8"')
        query_str = f.read()
    except FileNotFoundError:
        print('Please provide an input file that exists')
        sys.exit(1)
    query = generate_snopes_query(query_str)
    print(query)

    list_of_links = grab_links(query)

    print(list_of_links)
    for link in list_of_links:
        print(link)
        print(grab_rating(link))


if __name__ == "__main__":
    main(sys.argv[1:])