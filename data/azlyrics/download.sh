#!/bin/bash
#
#1: artists list file
#2: skip lines
#3: output folder

if [ $# -lt 3 ]; then
	echo "few arguments; $0 artist_list_file #skip output_folder"
	exit 1
fi

mkdir -p $3

COUNT=$2-1
while IFS=',' read -r slug url; do
	COUNT=$(( $COUNT + 1 ))
	echo "line $COUNT: $slug : $url"
	python ../../source/azlyrics/download_songs.py -m './meta.db' --artist "$slug" --filepath "$3${slug}.txt" -t 100 --tags "$COUNT: $slug : $url"
	echo "line $COUNT: $slug : $url" > download_status.txt

done < <(tail -n "+$2" "$1")
