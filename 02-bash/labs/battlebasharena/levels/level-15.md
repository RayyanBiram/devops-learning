# Level 15: Boss Battle 3 - Advanced Scripting

## Mission
Combine the skills you've gained! Write a script that:

1. Presents a menu to the user with the following options:

- Check disk space
- Show system uptime
- Backup a directory and keep the last 3 backups
- Parse a configuration file and display the values

2. Execute the chosen task.

## Script
```bash
#!/bin/bash

disk_space() {
        df -h
}

system_uptime() {
        uptime -p
        uptime -s
}

backup_directory() {
        local directory
        local backupdirectory

        echo "Enter a directory: "
        read directory

        if [ -z $directory ]; then
                echo "No input detected."
                exit 1
        elif [[ ! -d $directory ]]; then
                echo "Directory does not exist"
                echo "Enter a valid directory"
                exit 1
        else
                echo "Enter a backup directory: "
                read backupdirectory

                if [ -z $backupdirectory ]; then
                        echo "No input detected."
                        exit 1
                elif [[ ! -d $backupdirectory ]]; then
                        echo "Directory does not exist"
                        echo "Enter a valid directory"
                        exit 1
                else
                        size=$(ls $backupdirectory | wc -l)
                        if [[ $size -lt 3 ]]; then
                                cp -r $directory $backupdirectory/backup_$(date +%Y-%m-%d-%H-%M-%S)
                        else
                                oldestbackup=$(ls -tr $backupdirectory | head -1)
                                rm -r $backupdirectory/$oldestbackup
                                cp -r $directory $backupdirectory/backup_$(date +%Y-%m-%d-%H-%M-%S)
                        fi
                fi
        fi
}

config_file() {
        local file

        echo "Enter a file: "
        read file

        if [ -z $file ]; then
                echo "No input detected."
                exit 1
        elif [[ ! -f $file ]]; then
               echo "File does not exist"
               echo "Enter a valid filename"
                exit 1
        else
                awk -F= '{ print $1 "=" $2 }' $file
        fi
}

echo "
1) Check system disk space
2) Show system uptime
3) Backup a directory and keep the last 3 backups
4) Parse a configuration file and display the values

Choose what you would like to do: "

read choice

case $choice in
        1) echo "Checking disk space..." ; disk_space ;;
        2) echo "Displaying system uptime..." ; system_uptime ;;
        3) backup_directory ;;
        4) config_file ;;
        *) echo "Invalid option" ;;
esac
```

## Result
<img src="../images/level 15 - boss battle 3 - advanced scripting.png" width="700"/>