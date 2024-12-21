# Personal file to upload commits faster

#!/bin/bash

if [[ -z "$1" ]]; then
	echo "Provide message commit"
	exit 1
fi

git status

read -p "Continue? (y/n): " confirm

if [[ $confirm == "y" || $confirm == "Y" ]]; then
	git add .
	git commit -m "$1"
	git push origin
else
	echo "Cancelled"
	exit 1
fi
	
