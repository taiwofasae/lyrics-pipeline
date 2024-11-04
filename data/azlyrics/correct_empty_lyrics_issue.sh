#!/bin/bash
#
#1: input folder
#2: output folder

if [ $# -lt 2 ]; then
	echo "too few arguments; $0 input_folder output_folder"
	exit 1
fi

mkdir -p $2

for filepath in $1/*.csv; do
	prev="$filepath"
	next="$2/$(basename ${filepath})"
	
	echo "correcting '$prev' to '$next'"
	
	sed -z 's,"\n"\n"," \n"\n",g' "$prev" > "$next.temp"
	mv "$next.temp" "$next"
done
