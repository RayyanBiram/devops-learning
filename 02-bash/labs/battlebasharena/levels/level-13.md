# Level 13: Backup Script with Rotation

## Mission
Create a script that backs up a directory to a specified location and keeps only the last 5 backups.

## Script
```bash
#!/bin/bash

directory=$1
backupdirectory=$2

if [ $# -eq 0 ]; then
        echo "No input detected."
        echo "Example input: ./lvl13.sh directory backupdirectory"
        exit 1
elif [[ ! -d $directory ]]; then
        echo "Directory does not exist"
        echo "Enter a valid directory"
        echo "Example input: ./lvl13.sh directory backupdirectory"
        exit 1
elif [[ ! -d $backupdirectory ]]; then
        echo "Directory does not exist"
        echo "Enter a valid directory"
        echo "Example input: ./lvl13.sh directory backupdirectory"
        exit 1
else
        size=$(ls $backupdirectory | wc -l)
        if [[ $size -lt 5 ]]; then
                cp -r $directory $backupdirectory/backup_$(date +%Y-%m-%d-%H-%M-%S)
        else
                oldestbackup=$(ls -tr $backupdirectory | head -1)
                rm -r $backupdirectory/$oldestbackup
                cp -r $directory $backupdirectory/backup_$(date +%Y-%m-%d-%H-%M-%S)
        fi
fi
```

## Result
<img src="../images/level 13 - backup script with rotation.png" width="700"/>