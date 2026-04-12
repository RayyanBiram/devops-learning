# Level 5: The Boss Battle - Combining Basics

## Mission
Combine what you've learned! Write a script that:

1. Creates a directory named 'Battlefield'`
2. Inside Battlefield, create files named knight.txt, sorcerer.txt, and rogue.txt.
3. Check if knight.txt exists; if it does, move it to a new directory called Archive.
4. List the contents of both Battlefield and Archive.

## Script
```bash
#!/bin/bash

mkdir battlefield

touch battlefield/{knight,sorcerer,rogue}.txt

if [[ -f battlefield/knight.txt ]]; then
        mkdir archive
        cp battlefield/knight.txt archive/
fi

ls battlefield
ls archive
```

## Result
<img src="../images/level 5 - the boss battle - combining basics.png" width="700"/>