# Scenario: "The Command Line Murders"

## Objective
 This is the <a href="https://github.com/veltman/clmystery" target="_blank">Command Line Murders</a> with a small twist as in the solution is different.

Enter the name of the murderer in the file /home/admin/mysolution, for example echo "John Smith" > ~/mysolution.

Test: `md5sum ~/mysolution` returns `9bba101c7369f49ca890ea96aa242dd5`.

## Investigation
Used standard Linux text-processing and file inspection commands to search through files, filter content, and follow clues step by step.

## Commands used
```bash
ls
grep -e
sed -n
cat
grep -A
echo
```

## Result
<img src="../images/The Command Line Murders.png" width="700"/>