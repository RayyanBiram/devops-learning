# Level 8: Multi-File Searcher

## Mission
Create a script that searches for a specific word or phrase across all `.log` files in a directory and outputs the names of the files that contain the word or phrase.

## Script
```bash
#!/bin/bash

phrase="$1"
directory="$2"

if [ $# -eq 0 ]; then
        echo "No input detected."
        echo "Example input: ./lvl8.sh word directory"
        exit 1
elif [[ ! -d $directory ]]; then
        echo "Directory does not exist"
        echo "Enter a valid directory"
        echo "Example input: ./lvl8.sh word directory"
        exit 1
elif  ! ls $directory/*.log 1>/dev/null 2>/dev/null; then
        echo "No .log files in this directory"
        echo "Try another directory"
        exit 1
else
        grep -H -l -r --include="*.log" "$phrase" "$directory" 2>/dev/null
fi
```

## Result
<img src="../images/level 8 - multi-file searcher.png" width="700"/>