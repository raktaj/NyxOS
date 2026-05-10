# Changelog

All notable changes to NyxOS will be documented in this file.

---

## [v0.4] "Obscura"

### Added
- Permission model (`r`, `w`, `rw`, `none`) enforced across all FS operations
- `Permission` class with owner-based `check_read` / `check_write`
- `PermissionDenied` and `InvalidPermission` error types
- Root privilege bypass — root passes all permission checks system-wide
- `chmod` command — change file or directory permissions (owner only)
- `cp` command — copy file or directory (resets owner to copying user)
- `mv` command — move or rename file or directory
- `useradd` command — create new user with hashed credentials and home directory (root only)
- `passwd` command — change password (root can change any, users verify current first)
- `su` command — switch user mid-session with full context update
- `Session` dataclass in `shell.py` for mutable session state
- `SwitchUser` control flow exception for clean user switching
- `AuthenticationError` error type
- `UserStore` class — loads `users.json` once, exposes `get`, `create_user`, `change_password`, `_persist`
- `BootConfig` — reads `boot_config.json` on startup, writes defaults on first run
- `StorageProtocol` — `typing.Protocol` base for `JSONStorage` and `MemoryStorage`
- `initramfs` boot option — runs NyxOS with ephemeral `MemoryStorage` when `true`
- `user_store` added to `CommandContext`
- Per-user home directories (`/home/<username>`) created automatically on `useradd`
- `pwd()` fallback to `/` if home directory is missing

### Changed
- `fs.ls()` now returns full children dict (not just keys) for richer command output
- `ls.py` updated to use `fs.ls()` instead of `get_node` directly
- `get_node` now performs `check_read` before returning a node
- `write_file` preserves existing owner/mode on overwrite; sets current user on new files
- `fs.cwd` initialised to `/home/<username>` instead of hardcoded `/home/root`
- `FileSystem.__init__` now accepts `username` parameter
- `main.py` passes `username` into `FileSystem` after login
- `ctx` rebuilt each shell loop iteration to reflect current session user
- `parse_command` return type tightened — `args` is always `list[str]`, never `None`
- `CommandOutput.err` removed — all error paths now raise `NyxError` consistently

### Fixed
- Redirect logic in `shell.py` was inverted — `fs.write_file` now correctly runs in the redirect branch
- `cd.py` missing operand guard added
- `cd.py` no longer captures `None` return value of `fs.cd()`
- `tree.py` error handler now catches `NyxError` instead of `KeyError`
- `ls` plain output now uses sorted order matching styled output
- Stray `themer = Themer()` module-level instantiation removed from `themer.py`
- Duplicate permission validation removed from `fs.chmod` — delegates to `Permission.__init__`

---

## [v0.3] "Penumbra"

### Added
- Structured command output system (`CommandOutput`)
- Engine-agnostic theming system (Rich + prompt_toolkit adapters)
- Theme configuration via external JSON file
- Semantic coloring (directories vs files)

### Changed
- Refactored command architecture to return structured outputs
- Improved shell rendering pipeline (clean separation of logic and presentation)
- Updated `ls` with deterministic ordering (directories first, alphabetical)
- Improved prompt styling consistency across rendering engines

### Fixed
- Prompt color inconsistencies between Rich and prompt_toolkit
- Trailing newline issues in command output
- Incorrect `tree` traversal exposing internal filesystem structure

---

## [v0.2] "Umbra"

### Added
- Modular command system (commands decoupled from shell logic)
- Command context abstraction (`CommandContext`)
- Output redirection (`>`) support
- Depth-limited `tree` command with Rich rendering
- Enhanced filesystem commands (`rm -r`, improved errors)
- `neofetch` command with ASCII logo and system info

### Changed
- Improved prompt rendering and theming
- Cleaner internal architecture for future expansion (piping, scripting)

---

## [v0.1] "Tenebris"

### Added
- Initial shell implementation
- Basic filesystem abstraction
- Core commands (`cd`, `ls`, `pwd`, etc.)