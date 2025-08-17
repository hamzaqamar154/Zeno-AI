import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.ui_analyzer import UIAnalyzer
from src.suggestion_generator import SuggestionGenerator


def test_analyzer_initialization():
    analyzer = UIAnalyzer()
    assert analyzer.min_contour_area == 100
    print("✓ Analyzer initialization test passed")


def test_suggestion_generator():
    generator = SuggestionGenerator()
    assert len(generator.improvement_templates) > 0
    assert len(generator.best_practices) > 0
    print("✓ Suggestion generator test passed")


if __name__ == "__main__":
    test_analyzer_initialization()
    test_suggestion_generator()
    print("\nAll basic tests passed!")

