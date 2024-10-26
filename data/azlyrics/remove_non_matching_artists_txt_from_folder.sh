#!/bin/bash
#
# read arguments
#1: artists list txt
#2: artists song folder
#3: dump folder

if [ $# -lt 3 ]; then
        echo "few arguments; $0 artist_list_txt artists_song_folder dump_folder"
        exit 1
fi

artists_list=$1
song_folder=$2
dump_folder=$3
for songpath in $(ls -1 $song_folder*.txt); do

	filename=$(echo "$songpath" | sed -r 's/.*\/(.+).txt/\1/')
	artist=$(echo "$filename" | sed -r 's/(.*).txt/\1/')
	new_path="$dump_folder/$filename"
	match_string="$artist,"
	if grep -q "$match_string" "$artists_list"; then
		echo "$artist OK"
	else
		echo "Moving '$songpath' to '$new_path'"
		read -r -p "Proceed? <y/n> [y]: " proceed
		proceed=${proceed:-y}
		if [[ $proceed == "y" || $prompt == "Y" ]]; then
			mv $songpath "$new_path"
		fi
	fi
done
