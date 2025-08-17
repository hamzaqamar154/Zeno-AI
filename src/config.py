import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "output"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
MAX_IMAGE_SIZE = 10 * 1024 * 1024

ANALYSIS_CATEGORIES = [
    "layout",
    "color_scheme",
    "typography",
    "spacing",
    "accessibility",
    "user_flow"
]

SUGGESTION_TYPES = [
    "improvement",
    "best_practice",
    "accessibility",
    "modernization"
]

