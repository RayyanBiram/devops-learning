# 02 - Bash

Shell scripting with Bash - automating tasks, wiring commands together, and turning repetitive work into reliable, reusable scripts.

![OS](https://img.shields.io/badge/OS-Linux-232F3E?style=for-the-badge&logo=linux&logoColor=white)
![Bash](https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Focus](https://img.shields.io/badge/Focus-Automation-7B42BC?style=for-the-badge)
![Scripting](https://img.shields.io/badge/Practice-Scripting-FF9900?style=for-the-badge)

Bash is the default shell on most Linux systems and the glue that holds automation together. Rather than clicking through tasks by hand, you write a script. A plain text file of commands the shell runs top to bottom, and it does the work the same way every time. A script can create files, parse logs, back up directories, monitor a system, or chain dozens of small tools into one pipeline. That repeatability is why Bash sits underneath so much of DevOps: CI/CD steps, container entrypoints, cloud instance bootstrapping, and cron jobs are all, at heart, shell scripts. This folder contains two hands-on tracks - a level-based scripting game and a set of core automation challenges - each script written, tested, and documented in full.

## How Bash Works

- **Shebang** - the first line, `#!/bin/bash`, tells the system which interpreter runs the file.
- **Commands & pipelines** - each line runs a command. A pipe (`|`) feeds one command's output into the next, so small tools combine into bigger ones.
- **Variables** - store values with `name=value` and read them back with `$name`. Script arguments arrive as `$1`, `$2`, `$@`.
- **Conditionals & loops** - `if`, `case`, `for`, and `while` control the flow so a script can make decisions and repeat work.
- **Exit codes** - every command returns a status (`0` = success, non-zero = failure) that scripts check to handle errors.
- **Redirection** - `>` and `>>` send output to files, `2>` handles errors, and `< ` reads input from a file.

## Projects

| Project | What it builds | README |
|---------|----------------|--------|
| **Bash Battle Arena** | A 15-level scripting game - each level a "mission" solved with a script, ramping from file and directory basics through argument parsing, log searching, directory monitoring, backup rotation, and interactive menus, with a Boss Battle every 5 levels that combines the prior concepts | [View](labs/battlebasharena/README.md) |
| **Scripting Challenges** | Four core automation scripts - an arithmetic calculator, a file-operations automator, a file permission checker, and a timestamped backup script - plus a bonus system-monitor script that logs CPU, memory, disk, and top processes | [View](labs/scriptingchallenges/README.md) |

## What This Section Covers

- **File & directory operations** - creating, copying, moving, and listing files and directories
- **Variables & arithmetic** - storing values, command substitution with `$(...)`, and maths with `$((...))`
- **Control flow** - `if`/`elif`/`else`, `case` statements, and `for`/`while` loops
- **Argument & input handling** - positional parameters (`$1`, `$#`, `$@`) and interactive input with `read`
- **Validation & error handling** - checking inputs exist, guarding against empty values, and using exit codes
- **Text processing** - filtering and transforming output with `grep`, `awk`, `sort`, and `head`
- **System tasks** - disk usage (`df`/`du`), memory (`free`), processes (`ps`), and directory monitoring (`inotifywait`)
- **Automation patterns** - timestamped backups, retention/rotation, config parsing, and menu-driven scripts

## Core Concepts

| Concept | What it is |
|---------|------------|
| Shebang | The `#!/bin/bash` line that selects the interpreter for the script. |
| Variable | A named value - set with `name=value`, read with `$name`. |
| Positional parameter | An argument passed to the script - `$1`, `$2`, with `$#` as the count and `$@` as all of them. |
| Command substitution | Capturing a command's output into a value with `$(command)`. |
| Pipe | Feeding one command's output straight into the next with `|`. |
| Redirection | Sending output to a file (`>`, `>>`) or reading input from one (`<`). |
| Exit code | The success/failure status a command returns (`0` = success). |
| Test operator | A file or string check like `-d`, `-f`, `-r`, `-z` used inside `[[ ]]`. |

## Folder Structure

```
02-bash/
├── labs/
│   └── battlebasharena/          # 15-level Bash scripting game
│       ├── images/               # Screenshots of each level's output
│       ├── levels/               # level-01.md ... level-15.md (solutions)
│       └── README.md
└── labs/
    └── scriptingchallenges/          # Core automation challenges
        ├── challenges/               # challenge-01.md ... challenge-05.md
        ├── images/                   # Screenshots of each script's output
        └── README.md
```

## Key Commands

```bash
chmod +x script.sh          # make a script executable
./script.sh                 # run a script in the current directory
bash script.sh              # run a script explicitly with bash

echo "text" >> file.txt     # append a line to a file
grep "word" file.txt        # find lines containing a pattern
awk '{ print $1 }' file     # print a specific column
sort -n -k 5 file           # sort numerically by the 5th field
du -sh directory            # summarised, human-readable directory size
df -h                       # disk free across all filesystems
free -h                     # memory usage, human-readable
ps aux | sort -k 4 -nr      # processes sorted by memory usage

set -x                      # print each command as it runs (debugging)
set -e                      # exit immediately on any command failure
set -u                      # treat undefined variables as errors
```

## Basic Structure

A well-formed script starts with a shebang, validates its input, then does the work:

```bash
#!/bin/bash

# Store the first argument in a named variable
directory="$1"

# Validate before doing anything
if [ $# -eq 0 ]; then
    echo "No input detected."
    echo "Example: ./script.sh directory"
    exit 1
elif [[ ! -d $directory ]]; then
    echo "Directory does not exist"
    exit 1
else
    # Do the work once inputs are known good
    ls -l "$directory"/*.txt | sort -n -k 5 | awk '{ print $5, $9 }'
fi
```

Loops and command substitution let a script repeat work and capture results:

```bash
# Give each file a random number of lines (10-20)
for file in Arena_Boss/*.txt; do
    lines=$((RANDOM % 11 + 10))          # arithmetic expansion
    for i in $(seq 1 $lines); do
        echo "$i" >> "$file"
    done
done
```

## Best Practices

- **Start with `#!/bin/bash`** - never rely on the default shell being the one you tested against
- **Make scripts executable** - `chmod +x script.sh` before running with `./`
- **Quote your variables** - use `"$var"` not `$var` so paths with spaces don't break
- **Validate input early** - check arguments exist and files/directories are valid before acting
- **Use exit codes** - `exit 1` on failure so callers (and CI) can tell something went wrong
- **Prefer `[[ ]]` for tests** - it's safer and more capable than the older `[ ]`
- **Silence expected noise** - redirect errors with `2>/dev/null` only where you genuinely expect them
- **Add a timestamp to backups and logs** - `$(date +%Y-%m-%d-%H-%M-%S)` keeps every run unique
- **Keep backups outside the watched directory** - avoid feedback loops when monitoring changes
- **Comment the "why"** - explain intent, not the obvious mechanics of each line
- **Debug with `set -x`** - trace execution when a script misbehaves; `set -euo pipefail` hardens production scripts

## Resources

- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/)
- [Bash Reference (DevDocs)](https://devdocs.io/bash/)
- [ShellCheck](https://www.shellcheck.net/) - static analysis to catch common script bugs
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [explainshell](https://explainshell.com/) - breaks any command down flag by flag