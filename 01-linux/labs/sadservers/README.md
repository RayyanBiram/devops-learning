# SadServers

Linux troubleshooting scenarios on real, broken servers. Diagnose and fix live systems in a capture-the-flag format, against the clock.

![Scenarios](https://img.shields.io/badge/Scenarios-3%20%2F%203-brightgreen?style=for-the-badge)
![Linux](https://img.shields.io/badge/OS-Linux-232F3E?style=for-the-badge&logo=linux&logoColor=white)
![Troubleshooting](https://img.shields.io/badge/Focus-Troubleshooting-DD344C?style=for-the-badge)
![SRE](https://img.shields.io/badge/Skills-SRE%20%2F%20DevOps-7B42BC?style=for-the-badge)
![Practice](https://img.shields.io/badge/Practice-Hands--on-FF9900?style=for-the-badge)

[SadServers](https://sadservers.com/) is "like LeetCode, but for Linux". Instead of writing an algorithm, you're handed a real Linux server with something wrong on it and told to fix it. Each scenario spins up a throwaway cloud VM, gives you a browser terminal and a short brief, and a **"Check My Solution"** button that runs a test script to verify your fix. There's no multiple choice and no hand-holding: you investigate, form a hypothesis, and act, exactly like a real on-call incident. This folder documents three scenarios, a runaway process filling a disk, a log-analysis task, and a command-line investigation, each written up with the objective, the approach, and the commands used.

## How SadServers Works

- **Spin up** - each scenario boots a fresh, isolated Linux VM you reach through a browser-based terminal (no install, no SSH keys to manage).
- **Read the brief** - a short description states what's broken or what you need to find, plus how the solution is checked.
- **Investigate** - use standard Linux tools to work out what's happening: read logs, list processes, check disk and open files.
- **Fix or answer** - either repair the system (kill a process, restart a service) or write the answer into a specified file.
- **Check** - the "Check My Solution" button runs `/home/admin/agent/check.sh`, which you can read yourself to see exactly what's being tested.

## Scenarios

| Scenario | Level | What it's about | Write-up |
|----------|-------|-----------------|----------|
| **Saint John** | Easy | A rogue program is continuously writing to `/var/log/bad.log` and filling the disk. Find what's writing to it and stop it - without deleting the log file | [View](scenarios/saint-john.md) |
| **Saskatoon** | Easy | A web-server access log where each line starts with a requester's IP. Find the single IP with the most requests and write it to a solution file | [View](scenarios/saskatoon.md) |
| **The Command Line Murders** | Medium | A text-based investigation - sift through crime-scene files, follow the clues, and name the murderer, using only command-line text tools | [View](scenarios/the-command-line-murders.md) |

## What This Section Covers

- **Process management** - finding and terminating runaway processes with `ps`, `top`, `kill`, and `pkill`
- **Open files & disk** - tracing what's holding or writing a file with `lsof`, and checking space with `df` and `du`
- **Log analysis** - reading and following logs with `tail -f`, `cat`, `less`, and `journalctl`
- **Text processing** - filtering and counting with `grep`, `awk`, `cut`, `sort`, and `uniq -c`
- **Investigation** - chaining tools to follow a trail of clues across many files
- **Verification** - reading a check script to understand precisely what a "correct" fix looks like

## Documentation Structure

Each scenario is written up as `scenarios/scenario-name.md` with a consistent shape:

```
scenarios/
├── saint-john.md                  # Objective, Key Concepts, Commands Used, Result
├── saskatoon.md
└── the-command-line-murders.md

images/
└── scenario-name.png              # terminal screenshots for reference
```

Every write-up follows the same sections:

- **Objective** - what the scenario asks you to fix or find
- **Key Concepts** - the tools and ideas the scenario exercises
- **Commands Used** - the exact commands that solved it
- **Result** - confirmation the check passed (final answers redacted where they'd spoil the puzzle)

## Security Note

> [!IMPORTANT]
> Passwords, private keys, and sensitive data are **never committed** to GitHub. These write-ups document the *diagnostic approach*, how the problem was found and reasoned through, rather than just handing over answers. The scenarios are best experienced first-hand at [sadservers.com](https://sadservers.com/).

## Resources

- [SadServers](https://sadservers.com/) - the troubleshooting platform
- [SadServers Scenarios](https://sadservers.com/scenarios) - the full catalogue by difficulty and topic
- [The Command Line Murders](https://github.com/veltman/clmystery) - the original open-source mystery
- [explainshell](https://explainshell.com/) - breaks any command down flag by flag
- Man pages: `man <command>` (e.g. `man lsof`, `man kill`)