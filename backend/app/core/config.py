from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend/templates"
STATIC_DIR = BASE_DIR / "frontend" / "src"