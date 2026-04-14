# Level 9: Script to Monitor Directory Changes

## Mission
Write a script that monitors a directory for any changes (file creation, modification, or deletion) and logs the changes with a timestamp.

## Script
```bash
#!/bin/bash

# Command to be ran in tmux/screen/zellij when commands are needed to be ran in terminal

directory="$1"

if [[ $# -eq 0 ]]; then
        echo "Enter a directory"
        echo "Example: ./lvl9.sh /bashbattle/arena"
        exit 1
elif [[ ! -d $directory ]]; then
        echo "Directory not found"
        echo "Enter a valid directory"
        exit 1
else
        mkdir -p ../timestamp
        inotifywait -m -r -e create,delete,modify,move "$directory" | while read changes; do
                echo $(date) $changes >> ../timestamp/timestamp.txt
        done
fi
```

## Result
<img src="../images/level 9 - script to monitor directory changes" width="700"/>