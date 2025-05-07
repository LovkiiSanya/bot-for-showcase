from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


def load_text(name: str) -> str:
    file_path = (
        BASE_DIR / "product_bot" / "management" / "templates" / "texts" / "{}.txt".format(name)
    )
    with open(file_path, encoding="utf-8") as file:
        return file.read()
