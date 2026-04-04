# Scenario: "Saint John"

## Objective
A developer created a testing program that is continuously writing to a log file /var/log/bad.log and filling up disk. You can check for example with tail -f /var/log/bad.log. This program is no longer needed. Find it and terminate it. Do not delete the log file.

## Investigation
Checked which process had the log file open and was actively writing to it. Terminated the process with the PID.

## Commands used
```bash
tail -f /var/log/bad.log
lsof /var/log/bad.log
kill -9 588
```

## Result
<img src="../images/Saint John.png" width="700"/>