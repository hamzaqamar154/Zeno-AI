import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from ui_analyzer import UIAnalyzer
    from suggestion_generator import SuggestionGenerator
    from config import SCREENSHOTS_DIR
    print("✓ All core modules imported successfully")
    
    analyzer = UIAnalyzer()
    generator = SuggestionGenerator()
    print("✓ Analyzer and generator initialized successfully")
    print("✓ Project setup verified!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

