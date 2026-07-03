# 01 - Linux

Linux fundamentals - the operating system underneath nearly all of DevOps, learned hands-on through wargames and real broken-server scenarios.

![Linux](https://img.shields.io/badge/Linux-232F3E?style=for-the-badge&logo=linux&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GNU Bash](https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)
![SSH](https://img.shields.io/badge/SSH-000000?style=for-the-badge&logo=openssh&logoColor=white)
![OverTheWire](https://img.shields.io/badge/OverTheWire-Bandit-blue?style=for-the-badge)
![SadServers](https://img.shields.io/badge/SadServers-Troubleshooting-red?style=for-the-badge)

Linux is the operating system the modern cloud runs on. The vast majority of servers, containers, and cloud instances boot Linux, so being fluent at its command line is the foundation everything else in DevOps sits on. Instead of a graphical interface, you work through a **shell**, navigating the file system, managing permissions, wrangling processes, and chaining small tools together to get real work done. This folder builds that fluency the hands-on way, solving the OverTheWire Bandit wargame level by level, then debugging deliberately broken machines on SadServers. Every level and scenario is documented in full.

## How Linux Works

- **Everything is a file** - documents, directories, devices, and even processes are represented as files you can read, write, and pipe.
- **The shell** - a program (usually Bash) that reads your commands, runs them, and returns output. It's the primary interface to the system.
- **Permissions & ownership** - every file has an owner, a group, and read/write/execute bits that decide who can do what.
- **Processes** - every running program is a process with an ID (PID); you can list, inspect, prioritise, and kill them.
- **Pipes & redirection** - `|` feeds one command's output into the next, and `>`/`<` connect commands to files, so small tools combine into bigger ones.
- **SSH** - the secure way to reach a remote machine's shell over the network, the daily reality of working on servers you can't physically touch.

## Projects

| Project | What it covers | README |
|---------|----------------|--------|
| **OverTheWire: Bandit** | A 20+ level security wargame played entirely over SSH - each level hides a password reachable only by using the right command, ramping from basic navigation through file permissions, encoding/decoding, filtering, and network tools | [View](labs/overthewirebandit/README.md) |
| **SadServers** | Real "broken" Linux servers to diagnose and fix under time pressure - troubleshooting scenarios (Saint John, Saskatoon, The Command Line Murders) that build practical debugging and investigation skills | [View](labs/sadservers/README.md) |

## What This Section Covers

- **Navigation** - moving around the file system with `cd`, `ls`, `pwd`, and `find`
- **File operations** - reading, creating, copying, moving, and removing files and directories
- **Permissions & ownership** - reading `ls -l` output and changing access with `chmod` and `chown`
- **Text processing** - searching and transforming with `grep`, `cat`, `sort`, `cut`, and pipes
- **Encoding & compression** - decoding data and unpacking archives (`base64`, `gzip`, `tar`, `xxd`)
- **Processes** - listing and managing running programs with `ps`, `top`, and `kill`
- **Networking** - connecting and inspecting with `ssh`, `nc`, and `curl`
- **Troubleshooting** - investigating logs, disk, services, and permissions to fix broken systems

## Core Concepts

| Concept | What it is |
|---------|------------|
| Shell | The command interpreter (usually Bash) you type commands into. |
| File system | The tree of files and directories rooted at `/`. |
| Path | The location of a file - absolute (from `/`) or relative (from where you are). |
| Permissions | The read/write/execute bits controlling who can access a file. |
| Owner / group | The user and group a file belongs to. |
| Process | A running program, identified by a PID. |
| Pipe | `|` - sends one command's output into another as input. |
| Redirection | `>` / `>>` / `<` - connects commands to files for output or input. |
| SSH | Encrypted remote shell access to another machine. |

## Folder Structure

```
01-linux/
└── labs/
    ├── overthewirebandit/        # OverTheWire Bandit wargame
    │   ├── images/               # Screenshots of level solutions
    │   ├── levels/               # level-00.md ... level-20.md (walkthroughs)
    │   └── README.md
    └── sadservers/               # SadServers troubleshooting scenarios
        ├── images/               # Screenshots of the fixes
        ├── scenarios/            # saint-john.md, saskatoon.md, the-command-line-murders.md
        └── README.md
```

## Key Commands

```bash
# Navigation & files
pwd                         # print the current directory
ls -la                      # list all files, long format (permissions, owner, size)
cd /path/to/dir             # change directory
find / -name "secret*"      # search the whole tree for matching files
cat file.txt                # print a file's contents

# Permissions & ownership
chmod +x script.sh          # make a file executable
chmod 644 file.txt          # set read/write for owner, read for others
chown user:group file       # change a file's owner and group

# Text processing
grep "pattern" file         # find lines matching a pattern
sort file | uniq            # sort lines and remove duplicates
cut -d: -f1 /etc/passwd     # extract the first colon-separated field

# Encoding & archives
base64 -d file              # decode base64-encoded data
xxd file                    # view a file as hex
tar -xzf archive.tar.gz     # extract a gzipped tar archive

# Processes & networking
ps aux                      # list all running processes
top                         # live view of processes and resource usage
kill <PID>                  # stop a process by ID
ssh user@host -p 2220       # connect to a remote shell over SSH
nc host 30000               # open a raw network connection
```

## Basic Structure

A typical Linux workflow chains small tools together with pipes to answer a question in one line:

```bash
# Find the largest .log file in /var/log and show its size and name
ls -l /var/log/*.log | sort -n -k 5 | tail -1 | awk '{ print $5, $9 }'
```

`ls -l` output is the anchor for permissions and ownership - reading it fluently is core to Linux:

```
-rw-r--r--  1  rayyan  staff  1024  Apr 14  notes.txt
 │└─┬┘└─┬┘        │      │      │
 │  │   │         │      │      └── size in bytes
 │  │   │         │      └───────── group
 │  │   │         └──────────────── owner
 │  │   └────────────────────────── permissions for others (r--)
 │  └────────────────────────────── permissions for group   (r--)
 └───────────────────────────────── permissions for owner   (rw-)   (first char: - file, d directory)
```

## Best Practices

- **Read `ls -l` carefully** - permissions and ownership explain most "permission denied" problems
- **Use `man` and `--help`** - the answer is almost always in the manual (`man grep`, `curl --help`)
- **Know where you are** - be deliberate about relative vs absolute paths (`/` vs your current directory)
- **Pipe small tools together** - one focused command per stage beats one giant command
- **Be careful with `rm`** - there's no undo; double-check paths, especially with `rm -r`
- **Never store secrets in plain files** - and keep credentials out of anything you push to Git
- **Prefer SSH keys over passwords** - more secure and scriptable for remote access
- **Investigate before changing** - on a broken system, read logs and check state before editing anything

## Resources

- [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/) - the wargame used in this folder
- [SadServers](https://sadservers.com/) - hands-on Linux troubleshooting scenarios
- [The Linux Command Line (free book)](https://linuxcommand.org/tlcl.php)
- [explainshell](https://explainshell.com/) - breaks any command down flag by flag
- Man pages: `man <command>`