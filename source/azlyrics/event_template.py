

import argparse
from source.azlyrics import argparse_utils


def generate(template_file, artist, title, url, song, status=False):
    
    with open(template_file, "r", encoding='utf-8') as file:
        text = file.read()
    
    template = text.replace('#ARTIST', artist) \
    .replace('#TITLE', title) \
        .replace('#URL', url) \
            .replace('#SLUG', song) \
                .replace('#STATUS', f'{status}')
                
    return template

if __name__ == '__main__':
        
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '--template',
        type=str,
        required=True,
        help='Template file')
    
    parser.add_argument(
        '--artist',
        type=str,
        required=True,
        help='Artist')
    
    parser.add_argument(
        '--title',
        type=str,
        required=True,
        help='Song title')
    
    parser.add_argument(
        '--url',
        type=str,
        required=True,
        help='Song url')
    
    parser.add_argument(
        '--song',
        type=str,
        required=True,
        help='Song slug')
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Download status')
    
    args = parser.parse_args()
    
    print(generate(template_file=args.template,
                   artist=args.artist,
                   title=args.title,
                   url=args.url,
                   song=args.song,
                   status=args.status))
    
    