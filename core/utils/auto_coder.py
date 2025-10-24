from pathlib import Path

class AutoCoder:
    def __init__(self, base_path: str = "."):
        self.base = Path(base_path)

    def create_file(self, rel_path: str, content: str):
        p = self.base / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return str(p)
