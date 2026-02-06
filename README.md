# NyxOS

**NyxOS v0.2 “Umbra”**  
A terminal-based OS / VM simulation written in Python.

NyxOS simulates a UNIX-like environment with a virtual filesystem, interactive shell, and persistent state, focusing on structure, aesthetics, and extensibility rather than realism.

---

## Features
- UNIX-like shell
- JSON-backed virtual filesystem
- Persistent state
- Basic user model
- Rich-powered terminal UI
- Dark, minimal aesthetic

---

## What’s New in v0.2 “Umbra”
- Modular command system (commands decoupled from shell logic)
- Command context abstraction (`CommandContext`)
- Output redirection (`>`) support
- Depth-limited `tree` command with Rich rendering
- Enhanced filesystem commands (`rm -r`, improved errors)
- `neofetch` command with full ASCII logo and system info
- Improved prompt rendering and theming
- Cleaner internal architecture for future expansion (piping, scripting)

---

## Status
Active development (v0.2).  
Core systems are stabilizing, but APIs and behavior may still change.

---

## Roadmap (High-level)
- Command piping (`|`)
- Scripting / batch execution
- Permissions and ownership
- Process simulation
- Expanded system introspection

---

## License
MIT License
