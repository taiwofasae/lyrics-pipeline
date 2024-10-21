from bs4 import BeautifulSoup
import anon_requests as requests
import json
import string

agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) \
        Gecko/20100101 Firefox/24.0'
headers = {'User-Agent': agent}
base = "https://www.azlyrics.com/"

def clean_url(url_str):
    """
    Cleans a given URL.
    :param url_str: String formatted URL.
    :return: Cleaned string formatted URL.
    """
    url_str = url_str.lower()
    url_str = url_str.strip()

    

    # strip off trailing and leading '/'
    strips = [s.replace('//','/') for s in url_str.split('https://')]
    # extract last stem with valid address
    url_str = 'https://' + strips[-1]

    # remove protocol and subdomain www, then return
    url_str = url_str.split('https://')[-1]
    url_str = url_str.split('www.')[-1]
    url_str = 'https://www.' + url_str

    return url_str


def _get_html(url):
    if not url.startswith(base):
        url = base + url

    url = clean_url(url)

    response = requests.get(url, headers=headers)
    assert response.ok
    c = response.content
    print(f"response content length: {len(c)}")
    return c

def _get_letter_html(letter):
    if (letter.isalpha() and len(letter) == 1) or (letter == '19'):
        letter = letter.lower()
        url = base + letter + ".html"

        return _get_html(url)
    else:
        raise Exception("Unexpected Input")

def indexes():
    return [ch for ch in string.ascii_lowercase[:26]] + ['19']

def artists(letter, html_content = None):
    if not html_content:
        html_content = _get_letter_html(letter=letter)
   
    soup = BeautifulSoup(html_content, "html.parser")
    data = []

    for div in soup.find_all("div", {"class": "container main-page"}):
        links = div.findAll('a')
        for a in links:
            data.append((a.text.strip(), a['href']))
    return data

def _get_artist_page_html(artist, url = None):
    if url:
        return _get_html(base + url)
    
    artist = artist.lower().replace(" ", "")
    first_char = artist[0]
    url = base + first_char + "/" + artist + ".html"

    return _get_html(url)

def songs(artist, url = None, html_content = None):
    if not html_content:
        html_content = _get_artist_page_html(artist=artist, url = url)

    artist = artist.lower().replace(" ", "")

    artist = {
        'artist': artist,
        'albums': {},
        'songs': []
    }

    soup = BeautifulSoup(html_content, "html.parser")

    all_albums = soup.find('div', id='listAlbum')

    if not all_albums:
        return artist
    
    first_album = all_albums.find('div', class_='album')
    album_name = first_album.b.text
    s = []

    songs = []

    for tag in first_album.find_next_siblings(['a', 'div']):
        
        if tag.name == 'div' and tag.has_attr("class"):
            if "album" in tag['class']: # if album
                artist['albums'][album_name] = s
                s = []
                if tag.b is None:
                    pass
                elif tag.b:
                    album_name = tag.b.text

            else: # if song title
                if tag.text == "":
                    pass
                elif tag.text:
                    a_tag = tag.find_all('a', href=True)
                    s.append((tag.text, a_tag[0]['href'] if a_tag else None))
                    songs.append((tag.text, a_tag[0]['href'] if a_tag else None))

    artist['albums'][album_name] = s

    artist['songs'] = songs

    return artist

def _get_html_lyrics(artist, song):
    artist = artist.lower().replace(" ", "")
    song = song.lower().replace(" ", "")
    url = base + "lyrics/" + artist + "/" + song + ".html"

    return _get_html(url)

def lyrics(artist, song):

    artist = artist.lower().replace(" ", "")
    song = song.lower().replace(" ", "")

    return lyrics(_get_html_lyrics(artist, song))


def lyrics(html_content):

    soup = BeautifulSoup(html_content, "html.parser")
    l = soup.find_all("div", attrs={"class": None, "id": None})
    return [x.getText() for x in l] if l else []


def _read_html_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    return text

if __name__ == '__main__':
    j = _read_html_file('j.html')
    swift = _read_html_file('taylorswift.html')
    everybodylies = _read_html_file('everybodylies.html')
    #print(artists('j',html_content=j))
    #print(songs(artist = 'taylorswift', html_content = swift))
    #print(lyrics(everybodylies))