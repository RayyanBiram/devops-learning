# Level 3: Conditional Statements

## Mission
Write a script that checks if a file named `hero.txt` exists in the `Arena` directory. If it does, print `Hero found!`; otherwise, print `Hero missing!`.

## Script
```bash
#!/bin/bash

if [[ -f /home/rayyanbiram/bashbattle/arena/hero.txt ]]; then
        echo "Hero found!"
else
        echo "Hero missing!"
fi
```

## Result
<img src="../images/level 3 - conditional statements.png" width="700"/>