# Challenge 3: File Checker with Permissions

## Mission
Create a script that checks if a file exists and displays its permissions.

Requirements:

- Prompt user for a filename
- Check if the file exists
- If it exists, check if it's readable, writable, and executable
- Display appropriate messages for each permission

Example output:

Enter filename to check: /etc/passwd

File '/etc/passwd' exists. ✓ File is readable ✓ File is writable ✗ File is not executable

## Script
```bash
#!/bin/bash

echo -n "Enter filename to check: "
read filename

if [[ -z $filename ]]; then
        echo "No input detected."
        exit 1
elif [[ ! -f $filename ]]; then
        echo "Enter a valid filename."
        exit 1
else
        echo "File '$filename' exists."

        if [[ -r $filename ]]; then
                echo "✓ File is readable"
        else
                echo "✗ File is not readable"
        fi

        if [[ -w $filename ]]; then
                echo "✓ File is writable"
        else
                echo "✗ File is not writable"
        fi

        if [[ -x $filename ]]; then
                echo "✓ File is executable"
        else
                echo "✗ File is not executable"
        fi

fi
```

## Result
<img src="../images/file checker with permissions.png" width="700"/>