import re
import string

# lyrics cleaning helpers

class regex:
  PUNCTUATION = "[-\?.,\/#!$%\^&\*;:{}=\_~()]"
  TAGS = "\[(.*?)\]"
  REPEAT = 'x[0-9]+'
  CORRUPTED = r'[^\x00-\x7F]+'

class COLUMNS:
  ARTIST = 'artist'
  SONG_NAME = 'song'
  LYRICS = 'lyrics'
  CHAR_LENGTH = 'char_length'
  PUNCTATIONS = 'punctuations'
  TAGS = 'tags'
  CORRUPTED = 'corrupted'
  INSTRUMENTAL = 'instrumental'
  LINES = 'lines'
  BLOCKS = 'blocks'
  NEW_LINES = 'new_lines'
  N_BLOCKS = 'n_blocks'
  
def read_csv_max_split(filepath):
  output = []
  with open(filepath,"r", encoding='utf-8') as file:
    text = file.read()
  results = text.split('"\n"')


  [output.append([x.lstrip('\"').rstrip('\"') 
                  for x in line.rstrip().split('","',4)]) 
   for line in results]
  
  

  return output

def filter_songs(table):
  # Remove all songs without lyrics (e.g. instrumental pieces)
  table = table[table['lyrics'].str.strip().str.lower() != 'instrumental']

  # Remove any songs with corrupted/non-ASCII characters, unavailable lyrics
  table = table[~table['lyrics'].str.contains(regex.CORRUPTED)]
  table = table[table['lyrics'].str.strip() != '']
  if 'genre' in table.columns:
    table = table[table['genre'].str.lower() != 'not available']

  return table

def split_lyrics_into_lines(lyrics):
  return [x for x in lyrics.splitlines() if x.rstrip()]

def remove_empty_lines(lyrics):
  return '\n'.join(split_lyrics_into_lines(lyrics))

def count_punctuations1(lyrics):
  puncts = [(c, lyrics.count(c)) for c in string.punctuation]
  puncts = [cp for cp in puncts if cp[1] > 0]
  total = sum([p[1] for p in puncts])
  return total, puncts

def remove_punctuations1(lyrics):
  return lyrics.translate(str.maketrans('', '', string.punctuation))

def count_punctuations(lyrics):
  l = re.findall(regex.PUNCTUATION, lyrics)
  return len(l), [(x,l.count(x)) for x in set(l)]

def remove_punctuations(lyrics):
  return re.sub(regex.PUNCTUATION, ' ', lyrics)


def count_tags(lyrics):
  tags = re.findall(regex.TAGS,lyrics)
  return len(tags), tags

# remove song-related identifiers like [Chorus] or [Verse]
def remove_lyrics_taggings(lyrics):
  return re.sub(regex.TAGS, ' ', lyrics)


def count_songs_with_newline(table):
    with_lines = without_lines = num_newlines = 0
    for song in table['lyrics']:
        if "\n" in song:
            num_newlines += song.count("\n")
            with_lines += 1
        else:
            without_lines += 1
    return (with_lines, without_lines, with_lines + without_lines, float(num_newlines)/float(with_lines))

def split_lyrics_into_blocks(lyrics):
  lines = lyrics.splitlines()
  blocks = []
  b = []
  for line in lines:
    if line.strip():
      b.append(line)
    else:
      if b:
        blocks.append(b)
      b = []
  if b:
    blocks.append(b)

  return blocks

def clean_lyrics(lyrics):
  lyrics = remove_punctuations(lyrics)

  lyrics = remove_lyrics_taggings(lyrics)

  return lyrics


def extract_details(songs_df, artist = None):

  songs_df = songs_df.copy()

  songs_df[COLUMNS.CHAR_LENGTH] = songs_df[COLUMNS.LYRICS].apply(len)

  songs_df[COLUMNS.PUNCTATIONS] = songs_df[COLUMNS.LYRICS].apply(lambda x: count_punctuations(x)[0])

  songs_df[COLUMNS.TAGS] = songs_df[COLUMNS.LYRICS].apply(lambda x: count_tags(x)[0])

  songs_df[COLUMNS.NEW_LINES] = songs_df[COLUMNS.LYRICS].apply(lambda x: len(x.split('\n')))

  songs_df[COLUMNS.LINES] = songs_df[COLUMNS.LYRICS].apply(split_lyrics_into_lines)

  songs_df[COLUMNS.N_BLOCKS] = songs_df[COLUMNS.LYRICS].apply(split_lyrics_into_blocks).apply(len)

  if artist:
    songs_df = songs_df[songs_df[COLUMNS.ARTIST] == artist]
  

  return songs_df