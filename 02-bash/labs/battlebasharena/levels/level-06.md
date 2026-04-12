# Level 6: Argument Parsing

## Mission
Write a script that accepts a filename as an argument and prints the number of lines in that file. If no filename is provided, display a message saying 'No file provided'.

## Script
```bash
#!/bin/bash

file_path="$1"
count="0"

if [ $# -eq 0 ]; then
        echo "No file provided"
elif [ ! -f "$1" ]; then
        echo "File not found!"
else
        while IFS= read -r line; do
                ((count++))
        done < "$file_path"
echo "Number of lines in the file: $count"

fi
```

## Result
<img src="../images/level 6 - argument parsing.png" width="700"/>