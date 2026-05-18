# Level 10: Boss Battle 2 - Intermediate Scripting

## Mission
Write a script that:
1. Creates a directory called Arena_Boss.
2. Creates 5 text files inside the directory, named file1.txt to file5.txt.
3. Generates a random number of lines (between 10 and 20) in each file.
4. Sorts these files by their size and displays the list.
5. Checks if any of the files contain the word 'Victory', and if found, moves the file to a directory called Victory_Archive.

## Script
```bash
#!/bin/bash

mkdir -p arena_boss
touch arena_boss/file{1..5}.txt

for r in arena_boss/*.txt; do
        rnumber=$((RANDOM % 11 + 10))
        for i in $(seq 1 $rnumber); do
                echo $i >> $r
        done
done

ls -l arena_boss/*.txt | sort -n -k 5 | awk '{ print $5, $9 }'
mkdir -p victory_archive


for s in arena_boss/*.txt; do
        if grep -q "Victory" $s; then
                mv $s victory_archive
        fi
done
```

## Result
<img src="../images/level 10 - boss battle 2 - intermediate scripting.png" width="700"/>