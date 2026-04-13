# Level 7: File Sorting Script

## Mission
Write a script that sorts all `.txt` files in a directory by their size, from smallest to largest, and displays the sorted list.

## Script
```bash
#!/bin/bash

Directory="$1"

if [[ $# -eq 0 ]]; then
        echo "Directory undefined."
        echo "Enter a directory"
        exit 1
elif [[ ! -d $Directory ]]; then
        echo "Directory does not exit"
        echo "Enter a valid directory"
        exit 1
elif  ! ls $Directory/*.txt 1>/dev/null 2>/dev/null; then
        echo "No .txt files in this directory"
        echo "Try another directory"
        exit 1
else
        cd $Directory
        ls -l *.txt | sort -n -k 5 | awk '{ print $5, $9 }'
fi
```

## Result
<img src="../images/level 7 - file sorting script .png" width="700"/>