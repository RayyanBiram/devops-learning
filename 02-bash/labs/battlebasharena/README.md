# Bash Battle Arena

A level-based Bash scripting game. Each level a "mission" solved by writing a script, ramping from file basics up to interactive, multi-part automation.

![Levels](https://img.shields.io/badge/Levels-1--15-brightgreen?style=for-the-badge)
![Bash](https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)
![Linux](https://img.shields.io/badge/OS-Linux-232F3E?style=for-the-badge&logo=linux&logoColor=white)
![Focus](https://img.shields.io/badge/Focus-Automation-7B42BC?style=for-the-badge)
![Practice](https://img.shields.io/badge/Practice-Scripting-FF9900?style=for-the-badge)

Bash Battle Arena is a scripting game designed to teach Bash the hands-on way. It's organised into levels: each one sets a "mission" that must be solved by writing a script, and the difficulty climbs as you go, from creating files and looping through numbers up to argument parsing, log searching, directory monitoring, backup rotation, and interactive menus. Every fifth level is a **Boss Battle** that combines the concepts from the previous four into one larger script. There's no VM or website yet - solutions are written and tested locally, then documented here. This folder covers levels **1 through 15**, each with the mission, the approach, and the script.

## How Bash Battle Arena Works

- **Read the mission** - each level states a task, from "create three files" to "build an interactive system-admin menu".
- **Write a script** - solve it with a Bash script, using the concepts introduced so far plus whatever new tool the level demands.
- **Test locally** - run the script, feed it edge cases (missing arguments, invalid paths), and confirm it behaves.
- **Level up** - each level introduces one new idea, so the difficulty rises steadily rather than all at once.
- **Boss Battles** - every 5th level (5, 10, 15) combines the prior levels' skills into a single, larger challenge.

## Levels

| Level | Mission | Concept | Solution |
|-------|---------|---------|----------|
| 1 | Create the `Arena` directory with three files and list it | `mkdir`, `touch`, `ls` | [View](levels/level-01.md) |
| 2 | Output the numbers 1 to 10, one per line | Variables and loops | [View](levels/level-02.md) |
| 3 | Check whether `hero.txt` exists and report | Conditionals (`if`/`else`, `-f`) | [View](levels/level-03.md) |
| 4 | Copy all `.txt` files from `Arena` to `Backup` | File manipulation (`cp`) | [View](levels/level-04.md) |
| 5 | **Boss Battle** - create, check, move, and list files | Combining the basics | [View](levels/level-05.md) |
| 6 | Print a file's line count from an argument | Argument parsing (`$1`, `$#`, `wc -l`) | [View](levels/level-06.md) |
| 7 | Sort a directory's `.txt` files by size | `ls -l`, `sort`, `awk` | [View](levels/level-07.md) |
| 8 | Search `.log` files for a word and name the matches | `grep -l`, `--include` | [View](levels/level-08.md) |
| 9 | Monitor a directory and log changes with a timestamp | `inotifywait`, `while read`, `date` | [View](levels/level-09.md) |
| 10 | **Boss Battle** - generate, size-sort, and archive files | `$RANDOM`, `seq`, loops, `grep` | [View](levels/level-10.md) |
| 11 | Alert if a directory's disk usage exceeds a threshold | `du -s`, numeric tests (`-gt`) | [View](levels/level-11.md) |
| 12 | Parse a `KEY=VALUE` config file and print the pairs | `awk -F=` | [View](levels/level-12.md) |
| 13 | Back up a directory, keeping only the last 5 | Timestamped backups + rotation | [View](levels/level-13.md) |
| 14 | Interactive menu for common system tasks | `case`, functions, `df`/`uptime` | [View](levels/level-14.md) |
| 15 | **Boss Battle** - menu combining disk, uptime, backup, config | Functions + `case` + everything prior | [View](levels/level-15.md) |

## What This Section Covers

- **File & directory operations** - creating, copying, moving, and listing with `mkdir`, `touch`, `cp`, `mv`, `ls`
- **Variables & arithmetic** - command substitution `$(...)`, maths `$((...))`, and `$RANDOM`
- **Control flow** - `if`/`elif`/`else`, `case` statements, and `for`/`while` loops
- **Argument & input handling** - positional parameters (`$1`, `$#`) and interactive `read`
- **Validation & error handling** - guarding against missing arguments, invalid paths, and empty values with exit codes
- **Text processing** - `grep`, `awk`, `sort`, `head`, `wc` for filtering and transforming output
- **System tasks** - disk usage (`du`/`df`), uptime, and directory monitoring with `inotifywait`
- **Automation patterns** - timestamped backups with rotation, config parsing, and menu-driven scripts

## Documentation Structure

Each level is written up as `levels/level-XX.md` with a consistent shape:

```
levels/
├── level-01.md    # Objective, Key Concepts, Commands Used, Result
├── level-02.md
└── ...             # through level-15.md

images/
└── level-XX.png    # terminal screenshots of the working script
```

Every write-up follows the same sections:

- **Objective** - what the level's mission asks for
- **Key Concepts** - the Bash feature or command the level introduces
- **Commands Used** - the script and the commands that solved it
- **Result** - confirmation the script runs and produces the expected output

## Notes

> [!TIP]
> Attempt each level yourself before reviewing a solution. Reach for `man`, `--help`, and debugging flags like `set -x` when you get stuck - understanding *why* a command behaves the way it does matters more than memorising syntax.

> [!IMPORTANT]
> Screenshots are cleaned of anything sensitive (internal IPs, hostnames) before being committed. The scripts document the *approach*, not machine-specific details.

## Resources

- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/)
- [ShellCheck](https://www.shellcheck.net/) - static analysis to catch common script bugs
- [explainshell](https://explainshell.com/) - breaks any command down flag by flag
- Man pages: `man <command>` (e.g. `man inotifywait`, `man awk`)