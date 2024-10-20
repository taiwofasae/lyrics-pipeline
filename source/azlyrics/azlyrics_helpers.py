
#from source.azlyrics import azlyrics

def get_artist_slug(artist_url):
  return '/'.join(artist_url.split('/')[-1:]).split('.html')[0]

def generate_artist_slug(artist):
  artist = artist.lower().rstrip('/').lstrip('/')
  if len(artist.split('/')) > 1:
    return artist
  return artist[0] + "/" + artist

def generate_artist_url(artist_url):
  artist = generate_artist_slug(artist_url)

  if len(artist.split('.html')) > 1:
    artist = artist.split('.html')[0]

  return artist + ".html"

def load_artist_list(filename):
  artist_list = []
  with open(filename, 'r') as f:
    artist_list = f.read().splitlines()
  return artist_list

def save_artist_list(artist_list, filename):
  with open(filename, 'w') as f:
    f.write('\n'.join(artist_list))

def save_song_list(song_list, filename):
  song_list = [','.join(l) for l in song_list]
  with open(filename, 'w') as f:
    f.write('\n'.join(song_list))

def load_song_list(filename):
  with open(filename, 'r') as f:
    song_list = f.read().splitlines()
  return [l.split(',') for l in song_list]

def extract_song_list_from_artist_list(artist_list):
  song_list = [['ARTIST_NAME','ARTIST_URL','SONG_NAME','SONG_URL']]
  for artist in artist_list:
    artist_url = generate_artist_url(artist)
    songs = azlyrics.songs(artist, url=artist_url) #[('We were happy', '/lyrics/taylorswitft/wewerehappy.html')]#
    for song, url in songs:
      song_list.append([artist, artist_url, song, url])

  return song_list

def download_songs_for_songlist(song_list_df, save_fn = None):
  if str(song_list_df):
    song_list_df = pd.read_csv(song_list_df)

  if 'LYRICS' not in song_list_df.columns:
    song_list_df['LYRICS'] = ''

  for index, row in song_list_df.iterrows():
    url = row['SONG_URL']
    lyrics = row['LYRICS'] or ''
    if not lyrics:
      try:
        lyrics = azlyrics.lyrics(html_content=azlyrics._get_html(url))[0]
        song_list_df.loc[index, 'LYRICS'] = lyrics
        if save_fn:
          save_fn(song_list_df)
      except:
        pass

  return song_list_df
