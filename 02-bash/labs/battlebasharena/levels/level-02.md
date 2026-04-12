# Level 2: Variables and Loops

## Mission
Create a script that outputs the numbers 1 to 10, one number per line.

## Script
```bash
#!/bin/bash

number=1

while [ $number -le 10 ]
do
        echo "$number"
        ((number++))
done
```

## Result
<img src="../images/level 2 - variables and loops script.png" width="700"/>