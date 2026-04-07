# Scenario: "Saskatoon"

## Objective
 There's a web server access log file at /home/admin/access.log. The file consists of one line per HTTP request, with the requester's IP address at the beginning of each line (first column).

Find what's the IP address that has the most requests in this file (there's no tie; the IP is unique). Write the solution into a file /home/admin/highestip.txt. For example, if your solution is "1.2.3.4", you can do echo "1.2.3.4" > /home/admin/highestip.txt

The SHA1 checksum of the IP address sha1sum /home/admin/highestip.txt is 6ef426c40652babc0d081d438b9f353709008e93 (just a way to verify the solution without giving it away, we also accept the right IP with no ending newline in the file.)

## Investigation
Isolated first column, sorted by IP and iteration count, isolated sorted result and copied to file `highestip.txt`. Used `sha1sum` to verify correct hash.

## Commands used
```bash
awk '{print $1}' /home/admin/access.log | sort -nr | uniq -c | sort -nr | head -1 | awk '{print $2}' > /home/admin/highestip.txt
sha1sum /home/admin/highestip.txt
```

## Result
<img src="../images/saskatoon.png" width="700"/>