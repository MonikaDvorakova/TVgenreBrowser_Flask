import requests
import xml.etree.ElementTree as et
import datetime
from bs4 import BeautifulSoup
import time


def get_login():
    """It loads the login from the file."""
    with open('login.txt') as file:
        login = file.read().strip()
    return login


def download_TVlisting_xml(date, channels, url):
    """It downloads the xml format of the TV listing and returns root as
    an ElementTree object. It downloads xml for every selected channel
    and it saves it in a dictionary, which it returns."""
    login = get_login()
    xml_roots = {}
    for channel in channels:
        parameters = {'user': login, 'date': date, 'channel': channel}
        response = requests.get(url, params=parameters)
        response.encoding = 'utf-8'
        root = et.fromstring(response.text)
        print(root)
        xml_roots[channel] = root
    return xml_roots


def max_date_calculation():
    """It returns max_date, for which the TV-listing is available. It is used in html <input type=date"""
    return datetime.date.today() + datetime.timedelta(days=14)


def find_shows_genre(xml_roots, genre):
    """It looks up all movies in the TV listing of the channels and
    returns the name, the channel(s) and time of the broadcasting.
    """

    found_results = []
    for channel, root in xml_roots.items():
        for show in root:
            if show.find('zanr').text == genre:
                time = show.find('cas').text
                for branch in show.findall('nazvy'):
                    movie_name = branch.find('nazev').text
                    movie_dictionary = {}
                    movie_dictionary.update([('name', movie_name),
                                             ('channel', channel),
                                             ('time', time)]
                                            )
                    found_results.append(movie_dictionary)
    if found_results:
        return found_results
    else:
        print(f'There\'s no movie in the TVlisting for today.')


def find_hyperlink(soup):
    """It founds the first hyperlink in the section search-films,
    which corresponds to the searched movie.
    """
    soup_section = (soup.find(id='search-films')
                    .find(class_='ui-image-list js-odd-even'))
    href = soup_section.find('a').get('href')
    return href


def csfd_redirect(href):
    """It redirects to the page of the movie and it returns info about it."""
    url = 'http://csfd.cz'
    response = requests.get(url+href, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, "html.parser")
    rating = soup.find(class_='average').text
    genre = soup.find(class_='genre').text
    origin = soup.find(class_='origin').text
    text = soup.find(id='plots').find(class_='content').find('li').text.strip()
    return (rating, genre, origin, text)


def ask_csfd(found_results):
    """It makes request to csfd web. It found first hyperlink and it goes
    there and finds rating of the movie and its short descripion.
    """
    url = 'http://csfd.cz/hledat/'
    for dictionary in found_results:
        show = dictionary['name']
        parameters = {'q': show}
        response = requests.get(url, params=parameters, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, "html.parser")
        href = find_hyperlink(soup)
        rating, genre, origin, text = csfd_redirect(href)
        dictionary.update([('rating', rating), ('genre', genre),
                           ('origin', origin), ('text', text)]
                          )
        time.sleep(1)
    return found_results


def date_reformat(date):
    date_string = datetime.datetime.strptime(date, '%Y-%m-%d')
    return datetime.datetime.strftime(date_string, '%d.%m.%Y')
