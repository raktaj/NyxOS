# fs.py

import json

class FileSystem:
    def __init__(self, fs_path="fs.json"):
        with open(fs_path, "r", encoding="utf-8") as f:
            self.fs = json.load(f)

        self.cwd = "/home/root"
        self.fs_path = fs_path

    # Internal Helpers

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
            if node["type"] != "dir":
                raise NotADirectoryError(path)
            node = node["children"][part]

        return node

    def _resolve_parent(self, path):
        path = self._normalize(path)
        parent_path, name = path.rsplit("/", 1)
        parent = self._resolve(parent_path or "/")

        if parent["type"] != "dir":
            raise NotADirectoryError(parent_path)

        return parent, name

    def _save(self):
        with open(self.fs_path, "w", encoding="utf-8") as f:
            json.dump(self.fs, f, indent=2)

    # Public API

    def pwd(self):
        return self.cwd

    def ls(self, path=None):
        node = self._resolve(path or self.cwd)
        if node["type"] != "dir":
            raise NotADirectoryError(path)
        return list(node["children"].keys())

    def cd(self, path):
        node = self._resolve(path)
        if node["type"] != "dir":
            raise NotADirectoryError(path)
        self.cwd = self._normalize(path)

    def cat(self, path):
        node = self._resolve(path)
        if node["type"] != "file":
            raise IsADirectoryError(path)
        return node["content"]

    def mkdir(self, path):
        parent, name = self._resolve_parent(path)

        if name in parent["children"]:
            raise FileExistsError(path)

        parent["children"][name] = {
            "type": "dir",
            "children": {}
        }

        self._save()

    def touch(self, path):
        parent, name = self._resolve_parent(path)

        if name not in parent["children"]:
            parent["children"][name] = {
                "type": "file",
                "content": "",
                "owner": "root"
            }
            self._save()

    def rm(self, path, recurse=False):
        parent, name = self._resolve_parent(path)

        if name not in parent["children"]:
            raise KeyError(path)

        node = parent["children"][name]

        if node["type"] == "dir":
            if not recurse:
                raise IsADirectoryError(path)
            del parent["children"][name]
            self._save()
            return

        del parent["children"][name]
        self._save()

    def rmdir(self, path):
        parent, name = self._resolve_parent(path)

        if name not in parent["children"]:
            raise KeyError(path)

        node = parent["children"][name]

        if node["type"] != "dir":
            raise NotADirectoryError(path)

        if node["children"]:
            raise OSError("Directory not empty")

        del parent["children"][name]
        self._save()

    def write_file(self, path, content):
        parent, name = self._resolve_parent(path)

        if name in parent["children"] and parent["children"][name]["type"] == "dir":
            raise IsADirectoryError(path)

        parent["children"][name] = {
            "type": "file",
            "content": content,
            "owner": "root"
        }

        self._save()

    def get_node(self, path=None):
        return self._resolve(path or self.cwd)