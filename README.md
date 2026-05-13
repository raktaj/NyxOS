# NyxOS
![Version](https://img.shields.io/badge/version-v0.5%20Noctis-c253bc)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active%20development-orange)

**NyxOS v0.5 "Noctis"**
A terminal-based OS / VM simulation written in Python.

---

## Overview

NyxOS simulates a UNIX-like environment with a virtual filesystem, interactive shell, and persistent state.
The project prioritizes **clean architecture, aesthetics, and extensibility** over strict realism.

---

## Features

- UNIX-like interactive shell
- JSON-backed virtual filesystem with typed node structure
- Persistent system state via `BootConfig`
- **Permission model** — owner-based `r`, `w`, `rw`, `none` enforcement
- **Multi-user system** — `useradd`, `passwd`, `su`, per-user home directories
- **Root privileges** — root bypasses permission checks system-wide
- User authentication with PBKDF2-HMAC password hashing
- Rich-powered terminal UI
- Engine-agnostic theming system
- Modular command architecture with auto-discovery
- Output redirection (`>`)
- `cp`, `mv`, `chmod` support

---

## Commands

| Command | Description |
|---|---|
| `cat` | Display file contents |
| `cd` | Change directory |
| `chmod` | Change file permissions |
| `clear` | Clear the screen |
| `cp` | Copy file or directory |
| `echo` | Print text |
| `help` | Show available commands |
| `ls` | List directory contents |
| `mkdir` | Create directory |
| `mv` | Move or rename file or directory |
| `neofetch` | Show system information |
| `passwd` | Change user password |
| `pwd` | Print working directory |
| `rm` | Remove file or directory |
| `rmdir` | Remove empty directory |
| `shutdown` / `exit` / `quit` | Power off NyxOS |
| `su` | Switch user |
| `touch` | Create empty file |
| `tree` | Display directory tree |
| `userdel` | Delete a user |
| `useradd` | Create a new user |
| `which` | Locate a command |
| `whoami` | Show current user |

---

## Boot Configuration

NyxOS reads from `boot_config.json` on startup. Ships with sensible defaults:

```json
{
    "initramfs": false,
    "ramfile": "fs.json",
    "theme": "themes.json",
    "users_db": "users.json",
    "hostname": "NyxOS"
}
```

Setting `initramfs` to `true` runs NyxOS with an ephemeral in-memory filesystem — nothing is persisted to disk.

---

## Status

Active development (v0.5).
Core systems are stabilizing, but APIs and behavior may still change.

---

## License

MIT License