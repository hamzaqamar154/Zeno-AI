# Zeno AI - UX/UI Design Assistant

Hey there! This is my UX/UI Design Assistant project. It's a tool I built that helps analyze design screenshots and gives you feedback on layout, colors, spacing, and overall design quality. Pretty useful when you want a second opinion on your designs or need quick insights.

## What It Does

Basically, you upload a screenshot of your UI/UX design (or a wireframe), and the tool analyzes it to give you:

- **Layout stuff** - Whether you're using a grid, how aligned things are, that kind of thing
- **Colors** - Checks your color scheme, contrast, and picks out the main colors you're using
- **Spacing** - Looks at how consistent your spacing is and if you're using whitespace well
- **Suggestions** - Gives you recommendations sorted by priority (high/medium/low)
- **Wireframe ideas** - Suggests what components might work well

I built the interface with Streamlit because it's quick and doesn't require a ton of frontend work. Just works.

**Note:** My main focus was on the logic and analysis algorithms, not the UI. So I kept the interface minimal and simple - it does the job without all the fancy bells and whistles. The real work is in the image processing and analysis code.

## Getting Started

### What You Need

Just Python 3.8 or higher. Nothing fancy.

### Setup

1. Clone this repo or download the files
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

That should install everything you need (OpenCV, Streamlit, NumPy, etc.)

### Running the App

The easiest way is to use the web interface:

```bash
streamlit run ui/app.py
```

Then just open your browser to `http://localhost:8501` and you're good to go.

You can also use it from the command line if you prefer:

```bash
python src/main.py path/to/your/image.png [output.json]
```

## How to Use

1. **Upload an image** - Click the upload button and select a screenshot or wireframe (PNG, JPG, etc.)
2. **Click "Analyze Design"** - The tool will process your image (might take a minute or two)
3. **Review the results** - You'll see scores, metrics, and suggestions organized by priority
4. **Download reports** - You can download either a JSON file with all the data or a nicely formatted PDF report

You'll get:
- Overall score (0-1, higher is better)
- Layout scores and what type of layout it detected
- Color metrics (contrast, diversity, etc.)
- Spacing measurements
- Actual suggestions for what to improve

## Project Structure

Here's how I organized the code:

```
├── src/
│   ├── ui_analyzer.py          # Does the actual image analysis
│   ├── suggestion_generator.py  # Generates the recommendations
│   ├── pdf_report_generator.py  # Creates the PDF reports
│   ├── config.py                # Settings and paths
│   └── main.py                  # CLI entry point
├── ui/
│   └── app.py                   # The Streamlit web interface
├── data/
│   └── screenshots/             # Where uploaded images go
├── tests/                       # Some basic tests
└── docs/                        # Architecture docs if you're curious
```

## Technical Stuff

Under the hood, I'm using:
- **OpenCV** for image processing and detecting UI elements
- **scikit-learn** for color clustering (finding dominant colors)
- **Streamlit** for the web interface (makes it super easy to build UIs)
- **ReportLab** for generating PDF reports

The analysis works by detecting edges and contours in the image, analyzing the layout patterns, extracting color information, and measuring spacing between elements. Then it runs all that through some scoring algorithms to give you the feedback.

## What I Learned

This was a fun project. I learned:
- How to use OpenCV for actual image analysis (not just tutorials)
- Color clustering with K-means (had to debug this a few times)
- Streamlit is way easier than I thought for building UIs
- PDF generation is more annoying than it should be (ReportLab's stylesheet system is weird)
- How to structure a project so it doesn't become a mess

Also learned that image processing takes time, so I added loading spinners and progress messages so users don't think it's broken.

## Known Limitations

Fair warning:
- Works best with clear UI screenshots (not photos of screens or messy wireframes)
- If you have a ton of overlapping elements, it might get confused
- Big images take longer to process (I set a 10MB limit)
- The suggestions are just rule-based right now - not using any ML models. Could be better with actual training data, but that's a whole other project.

## Future Ideas

Some things I'm thinking about adding:
- Integration with Figma or Sketch
- Better ML models for more accurate pattern recognition
- Side-by-side comparison of multiple designs
- Export to different formats (not just PDF)
- Maybe a way to track design improvements over time

## Troubleshooting

If you run into issues:

- **PDF generation errors**: Make sure reportlab is installed (`pip install reportlab`)
- **Import errors**: Double-check that all dependencies are installed
- **Slow processing**: Large images take time, be patient or resize them first
- **Style errors**: If you see style-related errors, try restarting the app

## License

This is a personal project, so feel free to use it for learning. If you build something cool with it, let me know!

## Credits

Built by Mirza Noor Hamza

If you have questions or suggestions, feel free to reach out!
