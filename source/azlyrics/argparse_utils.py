import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--metadatadb', '-m',
    type=str,
    required=True,
    help='Metadata sqlite file path')

parser.add_argument(
    '--tries', '-t',
    type=int,
    default=5,
    help='No of request attempts allowed'
)

parser.add_argument(
    '--tags',
    type=str,
    default="",
    help='Extra comments or tags'
)
