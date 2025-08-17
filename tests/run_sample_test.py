import sys
from pathlib import Path
import json
from PIL import Image, ImageDraw
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from src.ui_analyzer import UIAnalyzer
from src.suggestion_generator import SuggestionGenerator
from src.config import SCREENSHOTS_DIR


def create_sample_screenshot():
    """Create a simple sample UI screenshot for testing"""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple UI layout
    # Header
    draw.rectangle([0, 0, 800, 80], fill='#2c3e50', outline='#34495e')
    draw.text((20, 30), "Sample UI Design", fill='white')
    
    # Navigation
    draw.rectangle([0, 80, 200, 600], fill='#ecf0f1', outline='#bdc3c7')
    
    # Main content area
    draw.rectangle([200, 80, 800, 600], fill='#ffffff', outline='#e0e0e0')
    
    # Content boxes
    draw.rectangle([220, 120, 380, 280], fill='#3498db', outline='#2980b9')
    draw.rectangle([400, 120, 560, 280], fill='#e74c3c', outline='#c0392b')
    draw.rectangle([580, 120, 740, 280], fill='#2ecc71', outline='#27ae60')
    
    # Text elements
    draw.text((240, 180), "Card 1", fill='white')
    draw.text((420, 180), "Card 2", fill='white')
    draw.text((600, 180), "Card 3", fill='white')
    
    # Footer
    draw.rectangle([200, 500, 800, 600], fill='#34495e', outline='#2c3e50')
    draw.text((220, 540), "Footer Content", fill='white')
    
    sample_path = SCREENSHOTS_DIR / "sample_ui.png"
    img.save(sample_path)
    return str(sample_path)


def run_sample_analysis():
    """Run analysis on sample screenshot and save results"""
    print("Creating sample UI screenshot...")
    sample_path = create_sample_screenshot()
    print(f"Sample screenshot created: {sample_path}")
    
    print("\nRunning UI analysis...")
    analyzer = UIAnalyzer()
    generator = SuggestionGenerator()
    
    try:
        analysis = analyzer.full_analysis(sample_path)
        suggestions = generator.generate_suggestions(analysis)
        wireframe_info = generator.generate_wireframe_suggestions(analysis)
        
        results = {
            'sample_image': str(sample_path),
            'analysis': analysis,
            'suggestions': suggestions,
            'wireframe_suggestions': wireframe_info,
            'formatted_suggestions': generator.format_suggestions(suggestions)
        }
        
        output_path = Path(__file__).parent / "test_output.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("AI UX/UI Design Assistant - Sample Test Output\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("SAMPLE IMAGE: " + str(sample_path) + "\n\n")
            
            f.write("ANALYSIS RESULTS:\n")
            f.write("-" * 60 + "\n")
            f.write(f"Overall Score: {analysis['overall_score']}/1.0\n")
            f.write(f"Layout Type: {analysis['layout']['layout_type']}\n")
            f.write(f"Elements Detected: {analysis['elements']['total_elements']}\n")
            f.write(f"Image Dimensions: {analysis['elements']['image_dimensions']}\n\n")
            
            f.write("LAYOUT METRICS:\n")
            f.write(f"  Grid Score: {analysis['layout']['grid_score']}\n")
            f.write(f"  Alignment Score: {analysis['layout']['alignment_score']}\n")
            f.write(f"  Symmetry Score: {analysis['layout']['symmetry_score']}\n\n")
            
            f.write("COLOR METRICS:\n")
            f.write(f"  Unique Colors: {analysis['colors']['unique_colors']}\n")
            f.write(f"  Contrast Score: {analysis['colors']['contrast_score']}\n")
            f.write(f"  Color Diversity: {analysis['colors']['color_diversity']:.2f}\n")
            f.write(f"  Dominant Colors: {analysis['colors']['dominant_colors'][:3]}\n\n")
            
            f.write("SPACING METRICS:\n")
            f.write(f"  Spacing Consistency: {analysis['spacing']['spacing_consistency']}\n")
            f.write(f"  Whitespace Ratio: {analysis['spacing']['whitespace_ratio']}\n")
            f.write(f"  Element Density: {analysis['spacing']['element_density']}\n\n")
            
            f.write("DESIGN SUGGESTIONS:\n")
            f.write("-" * 60 + "\n")
            f.write(generator.format_suggestions(suggestions, use_emojis=False))
            f.write("\n\n")
            
            f.write("WIREFRAME RECOMMENDATIONS:\n")
            f.write("-" * 60 + "\n")
            f.write("Recommended Structure:\n")
            for component, include in wireframe_info['structure'].items():
                status = "Include" if include else "Optional"
                f.write(f"  - {component.title()}: {status}\n")
            f.write("\nRecommendations:\n")
            for rec in wireframe_info['recommendations']:
                f.write(f"  - {rec}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("Test completed successfully!\n")
            f.write("=" * 60 + "\n")
        
        print(f"\n[OK] Analysis complete!")
        print(f"[OK] Results saved to: {output_path}")
        print(f"\nOverall Score: {analysis['overall_score']}/1.0")
        print(f"Layout Type: {analysis['layout']['layout_type']}")
        print(f"Elements Detected: {analysis['elements']['total_elements']}")
        print(f"\nGenerated {len(suggestions)} suggestions")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Running Sample Test - AI UX/UI Design Assistant")
    print("=" * 60 + "\n")
    
    success = run_sample_analysis()
    
    if success:
        print("\n" + "=" * 60)
        print("Sample test completed successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Sample test failed. Check errors above.")
        print("=" * 60)
        sys.exit(1)

