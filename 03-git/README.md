# 03 - Git

Version control with Git - tracking every change to your code, branching to work in parallel, and collaborating through GitHub.

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![SSH](https://img.shields.io/badge/SSH-000000?style=for-the-badge&logo=openssh&logoColor=white)
![pre-commit](https://img.shields.io/badge/pre--commit-FAB040?style=for-the-badge&logo=pre-commit&logoColor=black)

Git is the version control system nearly all software is built with. It is a tool that records the full history of a project as a series of snapshots, so you can see what changed, when, and why, and roll back to any earlier state. Rather than saving differences between versions, Git stores complete **snapshots** of your files, each identified by a SHA-1 hash and kept as an object inside the `.git` directory. That model is what makes branching cheap, merging reliable, and collaboration through GitHub possible. This folder documents the fundamentals: how Git stores history, the everyday commit workflow, branching and merging, and the collaboration patterns that make it the backbone of every DevOps toolchain.

## How Git Works

- **Snapshots, not diffs** - each commit is a complete picture of your files at that moment, not a list of changes; identical files are stored once and referenced.
- **Everything is an object** - Git stores three core object types: **blobs** (file contents), **trees** (directory structure), and **commits** (a snapshot plus metadata), each addressed by a SHA-1 hash.
- **The `.git` directory** - holds the whole repository: objects, refs (branch pointers), config, `HEAD` (where you are now), and the index (the staging area).
- **The three areas** - work flows from the **working directory** → `git add` → the **staging area** → `git commit` → the **repository**.
- **Branches are just pointers** - a branch is a lightweight, movable reference to a commit, which is why creating and switching branches is instant.
- **Remotes & GitHub** - a remote is a copy of the repo elsewhere (e.g. GitHub); you `push` your commits up and `pull` others' down.

## What You Should Know

| Area | What it covers |
|------|----------------|
| **Fundamentals** | Git tracks snapshots (not diffs), addresses everything by SHA-1 hash, and stores blobs, trees, and commits inside `.git` |
| **Core workflow** | Working directory → `git add` → staging area → `git commit` → repository, checked with `git status` |
| **File operations** | Removing (`git rm`), renaming (`git mv`), and undoing changes (`git restore`) |
| **History** | Viewing commits with `git log`, visualising with `--oneline --graph --all`, and inspecting with `git show` |
| **Differences** | `git diff` (unstaged), `git diff --staged` (staged), and `git blame` (line-by-line authorship) |
| **Branching & merging** | Creating and switching branches (`git switch -c`), combining them (`git merge`), and fast-forward vs recursive merges |
| **Conflict resolution** | Editing conflicted files, removing the `<<<<<<<` / `=======` / `>>>>>>>` markers, then staging and committing |
| **Rewriting history** | `git rebase` for a clean linear history, interactive rebase to squash/reorder, and `git commit --amend` |
| **Undoing safely** | `git restore`, `git reset` (`--soft` / `--mixed` / `--hard`), and `git revert` for a safe, non-destructive undo |
| **Collaboration** | The fork → clone → branch → commit → push → pull request → merge GitHub workflow |
| **Hygiene & security** | `.gitignore` patterns, pre-commit hooks, and keeping secrets out of history |

## Core Concepts

| Concept | What it is |
|---------|------------|
| Repository | The project and its complete history, stored in the `.git` directory. |
| Commit | A snapshot of the project at a point in time, with a message and a SHA-1 hash. |
| Blob / Tree / Commit | The three object types - file contents, directory structure, and snapshots. |
| Staging area (index) | The holding zone where changes wait between `git add` and `git commit`. |
| HEAD | A pointer to the commit (usually the branch tip) you're currently on. |
| Branch | A movable pointer to a commit - a cheap, independent line of work. |
| Remote | A copy of the repository elsewhere, such as `origin` on GitHub. |
| Merge vs rebase | Merge preserves branch history; rebase rewrites it into a clean line. |

## Essential Commands

```bash
# Setup
git config --global user.name "Name"            # set your commit author name
git config --global user.email "email@domain"   # set your commit email
ssh-keygen -t ed25519 -C "email"                # generate an SSH key for GitHub
ssh -T git@github.com                           # test the GitHub SSH connection

# Everyday workflow
git init                                        # start a new repository
git status                                      # see what's changed and staged
git add file                                    # stage a file
git commit -m "message"                         # save a snapshot
git log --oneline --graph --all                 # visual history of all branches
git diff                                        # unstaged changes
git diff --staged                               # staged changes
git blame file                                  # who last changed each line

# File operations
git rm file                                     # remove a tracked file
git mv old new                                  # rename/move a tracked file
git restore file                                # discard unstaged changes
git restore --staged file                       # unstage a file

# Branching & merging
git switch -c feature                           # create and switch to a branch
git switch main                                 # switch branches
git merge feature                               # merge a branch into the current one
git branch -d feature                           # delete a merged branch

# Remotes
git remote add origin <url>                     # link a GitHub remote
git push -u origin main                         # push and set upstream
git pull                                        # fetch + merge from the remote

# Saving & moving work
git stash                                       # shelve work in progress
git stash pop                                   # bring it back
git cherry-pick <commit>                        # copy one commit onto this branch

# Undoing
git commit --amend                              # fix the last commit
git reset --soft HEAD~1                         # undo a commit, keep changes staged
git revert <commit>                             # safely undo with a new commit
```

## Best Practices

- **Commit small and often** - one logical change per commit, with a clear message
- **Write meaningful messages** - explain *why*, not just *what*; use the imperative ("Add", "Fix")
- **Branch for every change** - keep `main` deployable and do work on feature branches
- **Pull before you push** - integrate others' changes to avoid surprise conflicts
- **Use a `.gitignore`** - exclude `*.log`, `node_modules/`, `.env`, build output, and local files
- **Never commit secrets** - keep credentials, keys, and `.env` files out of history entirely
- **Scan with pre-commit hooks** - automate checks with the pre-commit framework and tools like `git-secrets` or `trufflehog`
- **Prefer `git revert` over `reset` on shared branches** - it undoes safely without rewriting shared history
- **Review through pull requests** - assign reviewers and resolve conflicts before merging
- **Keep history readable** - use interactive rebase to squash noise before opening a PR

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/)
- [pre-commit](https://pre-commit.com/) - the framework for managing Git hooks
- [Oh Sh*t, Git!?!](https://ohshitgit.com/) - plain-English fixes for common Git mistakes