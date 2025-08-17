# System Architecture

## Overview

The AI UX/UI Design Assistant is built with a modular architecture that separates concerns into distinct components.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI Layer                    │
│                      (ui/app.py)                         │
│  - File upload handling                                  │
│  - Results visualization                                 │
│  - User interaction                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Analysis Engine                         │
│                (src/ui_analyzer.py)                      │
│  - Image loading & preprocessing                         │
│  - Element detection                                     │
│  - Layout analysis                                       │
│  - Color analysis                                        │
│  - Spacing analysis                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Suggestion Generator                        │
│          (src/suggestion_generator.py)                   │
│  - Rule-based suggestion generation                      │
│  - Priority assignment                                   │
│  - Wireframe recommendations                             │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### UI Analyzer (`src/ui_analyzer.py`)

**Responsibilities:**
- Load and preprocess images
- Detect UI elements using contour detection
- Analyze layout patterns (grid, horizontal, vertical, freeform)
- Extract and analyze color information
- Measure spacing consistency and whitespace

**Key Methods:**
- `load_image()`: Load image from file path
- `detect_elements()`: Find UI elements using edge detection
- `analyze_layout()`: Classify layout type and measure alignment
- `analyze_colors()`: Extract dominant colors and measure contrast
- `analyze_spacing()`: Calculate spacing metrics
- `full_analysis()`: Run complete analysis pipeline

### Suggestion Generator (`src/suggestion_generator.py`)

**Responsibilities:**
- Generate design improvement suggestions based on analysis
- Prioritize suggestions (high, medium, low)
- Provide wireframe structure recommendations
- Format suggestions for display

**Key Methods:**
- `generate_suggestions()`: Create prioritized suggestions from analysis
- `generate_wireframe_suggestions()`: Recommend wireframe structure
- `format_suggestions()`: Format suggestions for text output

### Configuration (`src/config.py`)

**Responsibilities:**
- Define project paths and directories
- Set allowed file types and size limits
- Define analysis categories and suggestion types

### Main Entry Point (`src/main.py`)

**Responsibilities:**
- CLI interface for command-line usage
- Orchestrate analysis and suggestion generation
- Output results to console or file

### Streamlit UI (`ui/app.py`)

**Responsibilities:**
- Provide web-based interface
- Handle file uploads
- Display analysis results visually
- Allow report downloads

## Data Flow

1. **Input**: User uploads image via Streamlit UI or CLI
2. **Processing**: Image is analyzed by UIAnalyzer
3. **Analysis**: Multiple metrics are calculated (layout, colors, spacing)
4. **Suggestion Generation**: SuggestionGenerator creates recommendations
5. **Output**: Results displayed in UI or saved to file

## Dependencies

- **OpenCV**: Computer vision and image processing
- **NumPy**: Numerical operations
- **Pillow**: Image handling
- **scikit-learn**: K-means clustering for color analysis
- **Streamlit**: Web interface framework

## File Storage

- `data/screenshots/`: Temporary storage for uploaded images
- `output/`: Generated analysis reports (if using CLI)
- `models/`: Reserved for future ML model storage

## Extension Points

The architecture supports easy extension:
- Add new analysis categories in `ui_analyzer.py`
- Add suggestion templates in `suggestion_generator.py`
- Integrate ML models by adding new analyzers
- Add export formats in the UI layer

