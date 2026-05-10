# fs.py

from errors import NoSuchFile, NotADirectory, IsADirectory, DirectoryNotEmpty, FileExists, PermissionDenied, InvalidPermission
from storage import StorageProtocol
from permissions import Permission, VALID_PERMISSIONS

class FileSystem:
    def __init__(self, storage: StorageProtocol, username: str = "root"):
        self.storage = storage
        self.fs = storage.load()
        self.cwd = f"/home/{username}"
        self.username = username

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
                raise NotADirectory(path)
            if part not in node["children"]:
                raise NoSuchFile(path)
            node = node["children"][part]

        return node

    def _resolve_parent(self, path):
        path = self._normalize(path)
        parent_path, name = path.rsplit("/", 1)
        parent = self._resolve(parent_path or "/")

        if parent["type"] != "dir":
            raise NotADirectory(parent_path)

        return parent, name

    def _save(self):
        self.storage.save(self.fs)

    # Public API

    def pwd(self):
        try:
            self._resolve(self.cwd)
        except NoSuchFile:
            self.cwd = "/"
        return self.cwd

    def ls(self, path=None):
        node = self._resolve(path or self.cwd)
        if node["type"] != "dir":
            raise NotADirectory(path)
        Permission.from_node(node).check_read(self.username, path or self.cwd)
        return node["children"]

    def cd(self, path):
        node = self._resolve(path)
        if node["type"] != "dir":
            raise NotADirectory(path)
        Permission.from_node(node).check_read(self.username, path)
        self.cwd = self._normalize(path)

    def cat(self, path):
        node = self._resolve(path)
        if node["type"] != "file":
            raise IsADirectory(path)
        Permission.from_node(node).check_read(self.username, path)
        return node["content"]

    def mkdir(self, path):
        parent, name = self._resolve_parent(path)

        if name in parent["children"]:
            raise FileExists(path)

        Permission.from_node(parent).check_write(self.username, path)

        parent["children"][name] = {
            "type": "dir",
            "children": {},
            "owner": self.username,
            "mode": "rw"
        }

        self._save()

    def touch(self, path):
        parent, name = self._resolve_parent(path)

        # Case: already exists
        if name in parent["children"]:
            node = parent["children"][name]

            if node["type"] == "dir":
                raise IsADirectory(path)

            # file exists → no-op (future: update timestamp)
            return

        Permission.from_node(parent).check_write(self.username, path)

        # Case: create new file
        parent["children"][name] = {
            "type": "file",
            "content": "",
            "owner": self.username,
            "mode": "rw"
        }

        self._save()

    def rm(self, path, recurse=False):
        parent, name = self._resolve_parent(path)

        if name not in parent["children"]:
            raise NoSuchFile(path)

        node = parent["children"][name]

        Permission.from_node(parent).check_write(self.username, path)

        if node["type"] == "dir":
            if not recurse:
                raise IsADirectory(path)
            del parent["children"][name]
            self._save()
            return

        del parent["children"][name]
        self._save()

    def rmdir(self, path):
        parent, name = self._resolve_parent(path)

        if name not in parent["children"]:
            raise NoSuchFile(path)

        node = parent["children"][name]

        if node["type"] != "dir":
            raise NotADirectory(path)

        if node["children"]:
            raise DirectoryNotEmpty(path)

        Permission.from_node(parent).check_write(self.username, path)

        del parent["children"][name]
        self._save()

    def chmod(self, path, mode):
        node = self._resolve(path)
        if node.get("owner") != self.username:
            raise PermissionDenied(path)
        if mode not in VALID_PERMISSIONS:
            raise InvalidPermission(mode)
        node["mode"] = mode
        self._save()

    def cp(self, src, dst):
        import copy
        src_node = self._resolve(src)
        Permission.from_node(src_node).check_read(self.username, src)

        dst_parent, dst_name = self._resolve_parent(dst)
        Permission.from_node(dst_parent).check_write(self.username, dst)

        if dst_name in dst_parent["children"]:
            node = dst_parent["children"][dst_name]
            if node["type"] == "dir":
                dst_parent = node
                dst_name = src.rsplit("/", 1)[-1]

        new_node = copy.deepcopy(src_node)
        new_node["owner"] = self.username  # reset owner to copying user
        dst_parent["children"][dst_name] = new_node
        self._save()

    def mv(self, src, dst):
        src_parent, src_name = self._resolve_parent(src)
        if src_name not in src_parent["children"]:
            raise NoSuchFile(src)

        src_node = src_parent["children"][src_name]
        Permission.from_node(src_node).check_read(self.username, src)
        Permission.from_node(src_parent).check_write(self.username, src)

        dst_parent, dst_name = self._resolve_parent(dst)
        Permission.from_node(dst_parent).check_write(self.username, dst)

        # if dst is an existing directory, move into it
        if dst_name in dst_parent["children"]:
            node = dst_parent["children"][dst_name]
            if node["type"] == "dir":
                dst_parent = node
                dst_name = src_name

        dst_parent["children"][dst_name] = src_node
        del src_parent["children"][src_name]
        self._save()

    def write_file(self, path, content):
        parent, name = self._resolve_parent(path)

        if name in parent["children"]:
            node = parent["children"][name]
            if node["type"] == "dir":
                raise IsADirectory(path)
            Permission.from_node(node).check_write(self.username, path)
            # overwrite — preserve existing owner and mode
            node["content"] = content
        else:
            Permission.from_node(parent).check_write(self.username, path)
            # new file — set owner to current user
            parent["children"][name] = {
                "type": "file",
                "content": content,
                "owner": self.username,
                "mode": "rw"
            }

        self._save()

    def get_node(self, path=None):
        node = self._resolve(path or self.cwd)
        Permission.from_node(node).check_read(self.username, path or self.cwd)
        return node