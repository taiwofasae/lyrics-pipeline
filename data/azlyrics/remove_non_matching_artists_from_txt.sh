#!/bin/bash
#
# read arguments
#1: artists list file

if [ $# -lt 1 ]; then
        echo "few arguments; $0 artist_list_file"
        exit 1
fi


filepath=$1
read -r -p "Filepath: $filepath. Proceed? <y/n> [y]: " proceed
proceed=${proceed:-y}
if [[ $proceed != "y" && $prompt != "Y" ]] then
	exit 0
fi
artist_letter=$(echo "$filepath" | sed -r 's/.*\/(.+).txt/\1/' | sed -r 's/(.*).txt/\1/')
blacklist_string=",$artist_letter"
sed -n "/$blacklist_string/p" $filepath > $filepath.temp
lines_changed=$(($(wc -l < $filepath)-$(wc -l < $filepath.temp)))
diff $filepath.temp $filepath > $filepath.temp.diff
less $filepath.temp.diff
rm $filepath.temp.diff
read -r -p "Approve removal? <y/n> [y]: " prompt
prompt=${prompt:-y}
if [[ $prompt == "y" || $prompt == "Y" ]] then
	echo "Lines changed in $filepath: $lines_changed; lines unchanged: $(wc -l < $filepath)"
	mv $filepath.temp $filepath
else
	exit 0
fi

