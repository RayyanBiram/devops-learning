# Level 12: Simple Configuration File Parser

## Mission
Write a script that reads a configuration file in the format KEY=VALUE and prints each key-value pair.

## Script
```bash
#!/bin/bash

file=$1

if [ $# -eq 0 ]; then
        echo "No input detected."
        echo "Example input: ./lvl12.sh filename"
        exit 1
elif [[ ! -f $file ]]; then
        echo "File does not exist"
        echo "Enter a valid filename"
        echo "Example input: ./lvl12.sh filename"
        exit 1
else
        awk -F= '{ print $1 "=" $2 }' $file
fi
```

## Result
<img src="../images/level 12 - simple configuration file parser.png" width="700"/>