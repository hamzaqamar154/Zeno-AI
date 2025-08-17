import sys
from pathlib import Path
import json
from ui_analyzer import UIAnalyzer
from suggestion_generator import SuggestionGenerator
from config import SCREENSHOTS_DIR, OUTPUT_DIR


def analyze_image(image_path: str, output_file: str = None):
    analyzer = UIAnalyzer()
    generator = SuggestionGenerator()
    
    print(f"Analyzing image: {image_path}")
    
    try:
        analysis = analyzer.full_analysis(image_path)
        suggestions = generator.generate_suggestions(analysis)
        wireframe_info = generator.generate_wireframe_suggestions(analysis)
        
        results = {
            'analysis': analysis,
            'suggestions': suggestions,
            'wireframe_suggestions': wireframe_info,
            'formatted_suggestions': generator.format_suggestions(suggestions)
        }
        
        if output_file:
            output_path = OUTPUT_DIR / output_file
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"Results saved to: {output_path}")
        
        print("\n=== ANALYSIS RESULTS ===")
        print(f"Overall Score: {analysis['overall_score']}/1.0")
        print(f"Layout Type: {analysis['layout']['layout_type']}")
        print(f"Elements Detected: {analysis['elements']['total_elements']}")
        print(f"\n=== SUGGESTIONS ===")
        print(generator.format_suggestions(suggestions))
        
        return results
        
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path> [output_file]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    analyze_image(image_path, output_file)

