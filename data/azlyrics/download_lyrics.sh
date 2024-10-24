#!/bin/bash
#
#1: artists list folder
#2: skip artists
#3: skip songs
#4: output folder

if [ $# -lt 4 ]; then
	echo "too few arguments; $0 artist_list_folder #skip artists #skip songs output_folder"
	exit 1
fi

mkdir -p $4

SKIP_A=$2-1
SKIP_B=$3-1
while read -r artist_path; do
	artist_slug=$(echo "$artist_path" | sed -r 's/.*\/(.+).txt/\1/')
	SKIP_A=$(( $SKIP_A + 1 ))
	output_file="$4$artist_slug.csv"
	if [[ ! -e $output_file ]]; then
		touch $output_file
		cat headers.txt  > $output_file
	fi
	while IFS='|' read -r song url; do
		SKIP_B=$(( $SKIP_B + 1 ))
		slug=$(echo "$url" | sed -r 's/.*\/(.+).html/\1/')
		echo "artist#$SKIP_A: $artist_slug | song#$SKIP_B:  $slug : $url"
		python ../../source/azlyrics/download_lyrics.py -m './meta.db' --artist "$artist_slug" --song "$slug" --filepath "${output_file%.*}.temp.csv" -t 100 --tags "artist#$SKIP_A: $artist_slug | song#$SKIP_B : $slug : $url"

		echo "\"$artist_slug\",\"\",\"$song\",\"$url\","+$(cat "${output_file%.*}.temp.csv") + "\"" >> $output_file
		break	
	done < <(tail -n "+$3" "$artist_path")
	break
done < <(ls $1*txt | tail -n "+$2")
