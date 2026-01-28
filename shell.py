from theme import PROMPT, MUTED, TEXT, ERROR, RESET
from fs import FileSystem

fs = FileSystem()

def run_shell(username):
    while True:
        cmd = input(f"{PROMPT}{username}@NyxOS{MUTED}:{fs.pwd()}{RESET}$ ")
        parts = cmd.split()

        if not parts:
            continue

        match parts[0].lower():
            case "shutdown":
                break

            case "pwd":
                print(TEXT + fs.pwd())

            case "ls":
                try:
                    for name in fs.ls(parts[1] if len(parts) > 1 else None):
                        print(name)
                except NotADirectoryError:
                    print(ERROR + "ls: not a directory")
                except KeyError:
                    print(ERROR + "ls: no such file or directory")

            case "cd":
                if len(parts) < 2:
                    print(ERROR + "cd: missing operand")
                    continue
                try:
                    fs.cd(parts[1])
                except NotADirectoryError:
                    print(ERROR + "cd: not a directory")
                except KeyError:
                    print(ERROR + "cd: no such file or directory")

            case "cat":
                if len(parts) < 2:
                    print(ERROR + "cat: missing operand")
                    continue
                try:
                    print(TEXT + fs.cat(parts[1]))
                except IsADirectoryError:
                    print(ERROR + "cat: is a directory")
                except KeyError:
                    print(ERROR + "cat: no such file")

            case "mkdir":
                if len(parts) < 2:
                    print(ERROR + "mkdir: missing operand")
                    continue
                try:
                    fs.mkdir(parts[1])
                except FileExistsError:
                    print(ERROR + "mkdir: file exists")
                except KeyError:
                    print(ERROR + "mkdir: invalid path")

            case "touch":
                if len(parts) < 2:
                    print(ERROR + "touch: missing operand")
                    continue
                try:
                    fs.touch(parts[1])
                except KeyError:
                    print(ERROR + "touch: invalid path")
            
            case "rm":
                if len(parts) < 2:
                    print(ERROR + "rm: missing operand")
                    continue
                try:
                    fs.rm(parts[1])
                except IsADirectoryError:
                    print(ERROR + "rm: is a directory")
                except KeyError:
                    print(ERROR + "rm: no such file")

            case "rmdir":
                if len(parts) < 2:
                    print(ERROR + "rmdir: missing operand")
                    continue
                try:
                    fs.rmdir(parts[1])
                except NotADirectoryError:
                    print(ERROR + "rmdir: not a directory")
                except KeyError:
                    print(ERROR + "rmdir: no such directory")
                except OSError:
                    print(ERROR + "rmdir: directory not empty")

            case "help":
                print(TEXT + "Available commands:")
                print(MUTED + "  pwd        print working directory")
                print(MUTED + "  ls         list directory contents")
                print(MUTED + "  cd         change directory")
                print(MUTED + "  cat        display file contents")
                print(MUTED + "  mkdir      create directory")
                print(MUTED + "  touch      create empty file")
                print(MUTED + "  rm         remove file")
                print(MUTED + "  rmdir      remove empty directory")
                print(MUTED + "  help       show this message")
                print(MUTED + "  shutdown   power off NyxOS")

            case _:
                print(ERROR + f"{parts[0]}: command not found")