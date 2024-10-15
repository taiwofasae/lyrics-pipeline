import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--metadatadb', '-m',
    type=str,
    required=True,
    help='Metadata sqlite file path')
