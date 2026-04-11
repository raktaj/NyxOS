# Changelog

All notable changes to NyxOS will be documented in this file.

---

## [v0.3] “Penumbra”

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

## [v0.2] “Umbra”

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