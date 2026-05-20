# Challenge 2: File Operations Script

## Mission
Create a script that automates directory and file creation.

Requirements:

- Create a directory called bash_demo
- Navigate into the directory
- Create a file called demo.txt
- Write text to the file (include current date)
- Display the file contents

Example output:

Directory 'bash_demo' created. File 'demo.txt' created.
File contents: This file was created by a Bash script on 2024-11-29

## Script
```bash
#!/bin/bash

mkdir bash_demo
cd bash_demo
touch demo.txt
echo "This file was created by a Bash script on $(date +%Y-%m-%d)" > demo.txt

echo "Directory 'bash_demo' created. File 'demo.txt' created."
echo -n "File contents: " && cat demo.txt
```

## Result
<img src="../images/file operations script.png" width="700"/>