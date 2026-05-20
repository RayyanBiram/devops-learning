# Challenge 4: Backup Script for Text Files

## Mission
Create a script that backs up all .txt files from one directory to another.

Requirements:

- Prompt user for source directory
- Create a backup directory if it doesn't exist
- Copy all .txt files to the backup directory
- Add timestamp to backup directory name
- Display count of files backed up

Example output:

Enter source directory: /home/user/documents
Backup directory created: backup_2024-11-29_14-30 Copying .txt files...
Backup complete! Files backed up: 5

## Script
```bash
#!/bin/bash

echo -n "Enter source directory: "
read directory

if [ -z $directory ]; then
        echo "No input detected."
        exit 1
elif [[ ! -d $directory ]]; then
        echo "Directory does not exist"
        echo "Enter a valid directory"
        exit 1
else
        backupdirectory=backup_$(date +%Y-%m-%d-%H-%M)
        mkdir $backupdirectory
        echo "Backup directory created: $backupdirectory"
        echo "Copying.txt files..."

        count=0
        for f in $directory/*.txt; do
                cp "$f" $backupdirectory/
                count=$((count + 1 ))
        done

        echo "Backup complete! Files backed up: $count"
fi
```

## Result
<img src="../images/backup script for text files.png" width="700"/>