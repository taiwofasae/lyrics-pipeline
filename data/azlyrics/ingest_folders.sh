#!/bin/bash
#

cd /home/taiwo/lyrics-pipeline/data/azlyrics/

cp azlyrics.csv "yesterday.csv"
cp azlyrics.sqlite "yesterday.sqlite"


# activate python myenv
source "../../source/azlyrics/myenv/bin/activate"

for dir in artists/*/
do
	dir=${dir%*/}
	echo "Ingesting... $dir"
	python ../../ingest/ingest_folder.py -f "$dir/" -e '.csv' -o "${dir%*/}.csv"
done

echo "Ingesting artists/ folder..."
rm azlyrics.sqlite
python ../../ingest/ingest_folder.py -f "artists/" -e ".csv" -o "azlyrics.csv" -db "azlyrics.sqlite"

echo "Done."

echo "Pushing to S3..."
date=$(date '+%Y-%m-%d')
python ../../storage/s3.py upload -d "raw/$date.csv" -s "azlyrics.csv"
python ../../storage/s3.py upload -d "raw/$date.sqlite" -s "azlyrics.sqlite"
#
# diff 
python ../../ingest/diff.py -c1 "yesterday.csv" -c2 "azlyrics.csv" -o "batch.csv" > diff.log
#
#deactivate venv
deactivate
