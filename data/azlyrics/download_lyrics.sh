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
SKIP_B=$3
while read -r artist_path; do
	echo "artist_path: $artist_path"
	artist_slug=$(echo "$artist_path" | sed -r 's/.*\/(.+).txt/\1/')
	SKIP_A=$(( $SKIP_A + 1 ))
	output_file="$4$artist_slug.csv"
	temp_output_file="${output_file%.*}.temp.csv"
	touch $temp_output_file

	cat headers.txt  > $output_file
	
	while IFS='|' read -r song url; do
		if [[ "$url" == 'None' ]]; then
			echo "'None' url found in text. Skipping..."
			continue
		fi
		slug=$(echo "$url" | sed -r 's/.*\/(.+).html/\1/')
		echo "artist#$SKIP_A: $artist_slug | song#$SKIP_B:  $slug : $url"
		python ../../source/azlyrics/download_lyrics.py -m './meta.db' --artist "$artist_slug" --song "$slug" --filepath "$temp_output_file" -t 100 --tags "artist#$SKIP_A: $artist_slug | song#$SKIP_B : $slug : $url"

		echo "\"$artist_slug\",\"\",\"$song\",\"$url\",\"" >> $output_file
		cat "$temp_output_file" >> $output_file
		echo "\"" >> $output_file
	
		SKIP_B=$(( $SKIP_B + 1 ))
	done < <(tail -n "+$SKIP_B" "$artist_path")
	SKIP_B=0 #reset songs counter
	rm "$temp_output_file"
done < <(ls $1*txt | tail -n "+$2")
