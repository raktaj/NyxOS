# boot.py

import json
from dataclasses import dataclass
from pathlib import Path

BOOT_CONFIG_PATH = "boot_config.json"

DEFAULTS = {
	"initramfs": False,
	"ramfile": "fs.json",
	"theme": "themes.json",
	"users_db": "users.json",
	"hostname": "NyxOS",
}

@dataclass
class BootConfig:
	initramfs: bool
	ramfile: str
	theme: str
	users_db: str
	hostname: str

	@staticmethod
	def load(path: str = BOOT_CONFIG_PATH) -> "BootConfig":
		config = dict(DEFAULTS)

		if Path(path).exists():
			with open(path, "r", encoding="utf-8") as f:
				overrides = json.load(f)
			config.update(overrides)
		else:
			# Write defaults on first boot
			with open(path, "w", encoding="utf-8") as f:
				json.dump(DEFAULTS, f, indent="\t")

		return BootConfig(**config)