# OverTheWire: Bandit

A beginner-friendly Linux security wargame. Learning the command line by hunting down passwords, one level at a time, entirely over SSH.

![Levels](https://img.shields.io/badge/Levels-0--20-brightgreen?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-232F3E?style=for-the-badge&logo=linux&logoColor=white)
![SSH](https://img.shields.io/badge/SSH-000000?style=for-the-badge&logo=openssh&logoColor=white)
![Focus](https://img.shields.io/badge/Focus-Linux%20Fundamentals-7B42BC?style=for-the-badge)
![Practice](https://img.shields.io/badge/Practice-Hands--on-FF9900?style=for-the-badge)

Bandit is [OverTheWire's](https://overthewire.org/wargames/bandit/) entry-level wargame, built to teach the Linux command line to absolute beginners. It's structured as a series of levels, each one hides the password for the *next* level somewhere on a remote server, and the only way to reach it is by using the right command. You SSH into the machine as `bandit<X>`, use what you find to progress, and the difficulty climbs from basic file reading up through permissions, encoding, filtering, and network tools. This folder documents levels **0 through 20**, each written up with the objective, the commands used, and the concept it teaches with passwords redacted.

## How Bandit Works

- **SSH in** - each level is a user (`bandit0`, `bandit1`, ...) you log into over SSH on `bandit.labs.overthewire.org` port `2220`.
- **Find the password** - the password for the next level is hidden on the server, in a file, encoded, buried in a directory, or behind a network port.
- **Use the right tool** - each level is designed so one command (or a short pipeline) reveals what you need.
- **Progress** - the password you find is the login for the next level, so you climb one rung at a time.
- **Learn by doing** - levels introduce a new concept each time, from `cat` and `find` to `grep`, `base64`, `ssh -i`, and `nc`.

## Levels

| Level | Concept | Walkthrough |
|-------|---------|-------------|
| 0 → 1 | SSH login - connecting to the game server | [View](levels/level-00.md) |
| 1 → 2 | Reading a file with an awkward name (`-`) | [View](levels/level-01.md) |
| 2 → 3 | Filenames with spaces | [View](levels/level-02.md) |
| 3 → 4 | Hidden (dotfile) files | [View](levels/level-03.md) |
| 4 → 5 | Identifying the human-readable file | [View](levels/level-04.md) |
| 5 → 6 | Finding a file by size and properties with `find` | [View](levels/level-05.md) |
| 6 → 7 | Finding a file by owner and group | [View](levels/level-06.md) |
| 7 → 8 | Searching text with `grep` | [View](levels/level-07.md) |
| 8 → 9 | Unique lines with `sort` and `uniq` | [View](levels/level-08.md) |
| 9 → 10 | Human-readable strings with `strings` | [View](levels/level-09.md) |
| 10 → 11 | Decoding Base64 | [View](levels/level-10.md) |
| 11 → 12 | ROT13 substitution with `tr` | [View](levels/level-11.md) |
| 12 → 13 | Hexdumps and repeated decompression | [View](levels/level-12.md) |
| 13 → 14 | SSH login with a private key | [View](levels/level-13.md) |
| 14 → 15 | Talking to a port with `nc` (netcat) | [View](levels/level-14.md) |
| 15 → 16 | Encrypted connections with `openssl s_client` | [View](levels/level-15.md) |
| 16 → 17 | Port scanning and picking the right service | [View](levels/level-16.md) |
| 17 → 18 | Comparing files with `diff` | [View](levels/level-17.md) |
| 18 → 19 | Running a command over SSH past a modified `.bashrc` | [View](levels/level-18.md) |
| 19 → 20 | Using a setuid binary to switch user | [View](levels/level-19.md) |
| 20 → 21 | Setuid binary + netcat + background jobs | [View](levels/level-20.md) |

## What This Section Covers

- **Navigation & file reading** - `cd`, `ls`, `pwd`, `cat`, `file`, and handling awkward filenames
- **Searching & filtering** - `find` by size/owner/type, `grep`, `sort`, `uniq`, and `strings`
- **Encoding & compression** - `base64`, `tr` (ROT13), `xxd`, and unpacking `gzip`/`bzip2`/`tar`
- **Permissions & ownership** - reading `ls -l`, fixing key permissions with `chmod`, and setuid binaries
- **SSH** - password and key-based login (`ssh -i`), ports, and running remote commands
- **Networking** - raw connections with `nc`, TLS with `openssl s_client`, and scanning with `nmap`
- **Redirection & pipes** - chaining tools together and sending errors to `/dev/null`

## Documentation Structure

Each level is written up as `levels/level-XX.md` with a consistent shape:

```
levels/
├── level-00.md    # Objective, Key Concepts, Commands Used, Result (redacted)
├── level-01.md
└── ...             # through level-20.md

images/
└── bandit-LX-X.png   # terminal screenshots for reference
```

Every walkthrough follows the same sections:

- **Objective** - what the level asks you to retrieve
- **Key Concepts** - the command(s) or idea the level teaches
- **Commands Used** - the exact commands that solved it
- **Result** - confirmation the password was found (the password itself is redacted)

## Security Note

> [!IMPORTANT]
> Passwords, private keys, and any sensitive data are **never committed** to GitHub. Each write-up documents the *method*, the commands and reasoning, not the flags. Anyone can (and should) reproduce the results by playing the game themselves.

## Resources

- [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/) - the wargame itself
- [OverTheWire Wargames](https://overthewire.org/wargames/) - where to go next (Natas, Leviathan, Krypton)
- [explainshell](https://explainshell.com/) - breaks any command down flag by flag
- Man pages: `man <command>`