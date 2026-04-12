# Level 4: File Manipulation

## Mission
Create a script that copies all `.txt` files from the `Arena` directory to a new directory called `Backup`.

## Script
```bash
#!/bin/bash

mkdir /home/rayyanbiram/bashbattle/arena/backup

for f in /home/rayyanbiram/bashbattle/arena/*.txt
do
        cp "$f" /home/rayyanbiram/bashbattle/arena/backup/
done
```

## Result
<img src="../images/level 4 - file manipulation.png" width="700"/>