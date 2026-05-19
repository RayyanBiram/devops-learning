# Level 14: User-Friendly Menu Script

## Mission
Create an interactive script that presents a menu with options for different system tasks (e.g., check disk space, show system uptime, list users), and executes the chosen task.

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

list_users() {
        users
}

echo "
1) Check system disk space
2) Show system uptime
3) List users

Choose what you would like to do: "

read choice

case $choice in
        1) echo "Checking disk space..." ; disk_space ;;
        2) echo "Displaying system uptime..." ; system_uptime ;;
        3) echo "Listing users" ; list_users ;;
        *) echo "Invalid option" ;;
esac
```

## Result
<img src="../images/level 14 - user-friendly menu script.png" width="700"/>