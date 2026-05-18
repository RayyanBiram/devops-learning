# Level 11: Automated Disk Space Report

## Mission
Create a script that checks the disk space usage of a specified directory and sends an alert if the usage exceeds a given threshold.

## Script
```bash
#!/bin/bash

directory="$1"
threshold="$2"

if [ $# -eq 0 ]; then
        echo "No input detected."
        echo "Example input: ./lvl11.sh directory threshold"
        exit 1
elif [[ ! -d $directory ]]; then
        echo "Directory does not exist"
        echo "Enter a valid directory"
        echo "Example input: ./lvl11.sh directory threshold"
        exit 1
elif [[ $threshold -lt 0 ]]; then
        echo "Threshold cannot be lower than 0"
        exit 1
else
        size=$(du -s $directory | awk '{ print $1 }')
        if [[ $size -gt $threshold ]]; then
                echo "Alert: Disk Usage exceeds the threshold"
        else
                echo $size
        fi
fi
```

## Result
<img src="../images/level 11 - automated disk space report.png" width="700"/>