# fs.py
import json

class FileSystem:
    def __init__(self, fs_path="fs.json"):
        with open(fs_path, "r", encoding="utf-8") as f:
            self.fs = json.load(f)

        self.cwd = "/home/root"
        self.fs_path = fs_path

    # --- internal helpers ---

    def _normalize(self, path):
        if path.startswith("/"):
            parts = path.strip("/").split("/")
        else:
            parts = self.cwd.strip("/").split("/") + path.split("/")

        stack = []
        for part in parts:
            if part in ("", "."):
                continue
            if part == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(part)

        return "/" + "/".join(stack)

    def _resolve(self, path):
        path = self._normalize(path)
        node = self.fs["/"]

        if path == "/":
            return node

        for part in path.strip("/").split("/"):
            node = node[part]

        return node

    def _resolve_parent(self, path):
        path = self._normalize(path)
        parent_path, name = path.rsplit("/", 1)
        parent = self._resolve(parent_path or "/")
        return parent, name

    def _save(self):
        with open(self.fs_path, "w", encoding="utf-8") as f:
            json.dump(self.fs, f, indent=2)

    # --- public API ---

    def pwd(self):
        return self.cwd

    def ls(self, path=None):
        node = self._resolve(path or self.cwd)
        if isinstance(node, dict):
            return list(node.keys())
        raise NotADirectoryError(path)

    def cd(self, path):
        node = self._resolve(path)
        if not isinstance(node, dict):
            raise NotADirectoryError(path)
        self.cwd = self._normalize(path)

    def cat(self, path):
        node = self._resolve(path)
        if isinstance(node, str):
            return node
        raise IsADirectoryError(path)

    def mkdir(self, path):
        parent, name = self._resolve_parent(path)

        if name in parent:
            raise FileExistsError(path)

        parent[name] = {}
        self._save()

    def touch(self, path):
        parent, name = self._resolve_parent(path)

        if name not in parent:
            parent[name] = ""
            self._save()
            
    def rm(self, path):
        parent, name = self._resolve_parent(path)

        if name not in parent:
            raise KeyError(path)

        if isinstance(parent[name], dict):
            raise IsADirectoryError(path)

        del parent[name]
        self._save()

    def rmdir(self, path):
        parent, name = self._resolve_parent(path)

        if name not in parent:
            raise KeyError(path)

        node = parent[name]

        if not isinstance(node, dict):
            raise NotADirectoryError(path)

        if node:
            raise OSError("Directory not empty")

        del parent[name]
        self._save()