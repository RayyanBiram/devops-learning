# Challenge 5: System Monitor Script

## Mission
Create a script that displays:

- Current CPU usage
- Memory usage (total, used, free)
- Disk usage
- Top 5 processes by memory
- Save the output to a log file with timestamp

## Script
```bash
#!/bin/bash

logfile=logfile_$(date +%Y-%m-%d-%H-%M-%S)
touch $logfile

echo -n "Current CPU usage: " >> $logfile
echo $(top -bn1 | grep "%Cpu" | awk '{ print $2 }') >> $logfile

echo -n "Current memory usage (total, used, free): " >> $logfile
echo $(free -h | grep "Mem:" | awk '{ print $2, $3, $4 }') >> $logfile

echo "Current disk usage: " >> $logfile
df -h >> $logfile

echo "Top 5 processes by memory: " >> $logfile
ps aux | sort -k 4 -nr | head -n 5 >> $logfile

echo "'$logfile' has been saved"
```

## Result
<img src="../images/system monitor script.png" width="700"/>