# Bash Scripting Challenges

A set of self-contained automation scripts, each solving a real, everyday task a Linux user or engineer actually hits, from arithmetic and file setup to permission checks, backups, and system monitoring.

![Scripts](https://img.shields.io/badge/Scripts-5-brightgreen?style=for-the-badge)
![Bash](https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)
![Linux](https://img.shields.io/badge/OS-Linux-232F3E?style=for-the-badge&logo=linux&logoColor=white)
![Focus](https://img.shields.io/badge/Focus-Automation-7B42BC?style=for-the-badge)
![Practice](https://img.shields.io/badge/Practice-Scripting-FF9900?style=for-the-badge)

A collection of practical Bash scripts, each one built around a task automation is genuinely good at. Doing arithmetic on user input, scaffolding files and directories, checking file permissions, backing up data with timestamps, and reporting on system health. Every script takes input, validates it, does the work, and reports back clearly, the same shape you'd want in any production automation. Together they cover the core building blocks of shell scripting: variables, arithmetic, conditionals, loops, user input, file operations, and text processing. This folder documents five scripts, each with its purpose, the approach, and the commands used.

## How These Scripts Work

- **Take input** - either interactively with `read` or as command-line arguments.
- **Validate first** - check the input exists and is sensible (a real number, an existing file) before doing anything.
- **Do the work** - perform the calculation, create the files, check the permissions, run the backup, or gather the metrics.
- **Report clearly** - print a readable result, and where relevant, write it to a file or log.
- **Handle the edge cases** - division by zero, missing files, empty input, and directories that don't exist yet.

## Scripts

| Script | What it does | Write-up |
|--------|--------------|----------|
| **Arithmetic Calculator** | Prompts for two numbers and prints all four operations - add, subtract, multiply, divide - with a guard against division by zero | [View](challenges/challenge-01.md) |
| **File Operations** | Scaffolds a `bash_demo` directory, creates `demo.txt` inside it, writes a dated line into it, and prints the contents back | [View](challenges/challenge-02.md) |
| **File Permission Checker** | Prompts for a filename, confirms it exists, then reports whether it's readable, writable, and executable | [View](challenges/challenge-03.md) |
| **Text-File Backup** | Prompts for a source directory, creates a timestamped backup directory, copies every `.txt` file across, and reports how many were backed up | [View](challenges/challenge-04.md) |
| **System Monitor** | Snapshots CPU usage, memory (total/used/free), disk usage, and the top 5 processes by memory - saving it all to a timestamped log file | [View](challenges/challenge-05.md) |

## What This Section Covers

- **User input & arguments** - reading interactive input with `read` and validating it before use
- **Arithmetic** - integer maths with `$((...))` and handling division by zero
- **File & directory operations** - creating, writing to, copying, and listing files and directories
- **Permissions** - testing access with `-r`, `-w`, `-x` and reading the result back to the user
- **Validation & error handling** - guarding against empty input, missing files, and absent directories
- **Timestamps** - stamping backups and logs with `date` so every run is unique
- **System reporting** - pulling live metrics from `top`, `free`, `df`, and `ps`
- **Text processing** - shaping command output with `grep`, `awk`, `sort`, and `head`

## Documentation Structure

Each script is written up as `challenges/challenge-XX.md` with a consistent shape:

```
challenges/
├── challenge-01.md    # Objective, Key Concepts, Commands Used, Result
├── challenge-02.md
└── ...                 # through challenge-05.md

images/
└── script-name.png     # terminal screenshots of the working script
```

Every write-up follows the same sections:

- **Objective** - what the script sets out to do
- **Key Concepts** - the Bash features and commands it uses
- **Commands Used** - the script and the commands that solved it
- **Result** - confirmation the script runs and produces the expected output

## Notes

> [!TIP]
> Every script starts with `#!/bin/bash` and is made executable with `chmod +x`. Variables are quoted (`"$var"`), input is validated before use, and comments explain the intent - the same habits that keep production automation reliable.

> [!IMPORTANT]
> Screenshots are cleaned of anything sensitive (internal IPs, hostnames) before being committed. The System Monitor output in particular is scrubbed, since it lists mounted filesystems.

## Resources

- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/)
- [Bash Reference (DevDocs)](https://devdocs.io/bash/)
- [ShellCheck](https://www.shellcheck.net/) - static analysis to catch common script bugs
- [explainshell](https://explainshell.com/) - breaks any command down flag by flag
- Man pages: `man <command>` (e.g. `man free`, `man ps`)
