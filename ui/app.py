import streamlit as st
import sys
from pathlib import Path
import json
from PIL import Image
import io

sys.path.append(str(Path(__file__).parent.parent))

from src.ui_analyzer import UIAnalyzer
from src.suggestion_generator import SuggestionGenerator
from src.pdf_report_generator import PDFReportGenerator
from src.config import SCREENSHOTS_DIR, ALLOWED_EXTENSIONS, MAX_IMAGE_SIZE


st.set_page_config(
    page_title="Zeno AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <h1 style='text-align: center; margin-bottom: 10px;'><span style='color: #3498db;'>Zeno AI</span> - UX/UI Design Assistant</h1>
    <h3 style='text-align: center; margin-top: 0; margin-bottom: 20px;'>by <span style='color: #7f8c8d;'>Mirza Noor Hamza</span></h3>
    """, unsafe_allow_html=True)
st.markdown("Upload a screenshot or wireframe to get AI-powered design analysis and suggestions")

if 'analyzer' not in st.session_state:
    st.session_state.analyzer = UIAnalyzer()
    st.session_state.generator = SuggestionGenerator()
    st.session_state.pdf_generator = PDFReportGenerator()

uploaded_file = st.file_uploader(
    "Choose an image file",
    type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
    help="Upload a UI/UX screenshot or wireframe for analysis"
)

if uploaded_file is not None:
    file_ext = Path(uploaded_file.name).suffix.lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        st.error(f"Unsupported file type. Please upload: {', '.join(ALLOWED_EXTENSIONS)}")
    else:
        image_bytes = uploaded_file.read()
        
        if len(image_bytes) > MAX_IMAGE_SIZE:
            st.error(f"File too large. Maximum size: {MAX_IMAGE_SIZE / (1024*1024):.1f} MB")
        else:
            image = Image.open(io.BytesIO(image_bytes))
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Uploaded Image")
                st.image(image)
                
                temp_path = SCREENSHOTS_DIR / uploaded_file.name
                with open(temp_path, 'wb') as f:
                    f.write(image_bytes)
            
            with col2:
                st.subheader("Analysis")
                
                if st.button("Analyze Design", type="primary"):
                    with st.spinner("Analyzing your design... please wait this may take a few minutes"):
                        try:
                            analysis = st.session_state.analyzer.full_analysis(str(temp_path))
                            suggestions = st.session_state.generator.generate_suggestions(analysis)
                            wireframe_info = st.session_state.generator.generate_wireframe_suggestions(analysis)
                            
                            st.session_state.analysis = analysis
                            st.session_state.suggestions = suggestions
                            st.session_state.wireframe_info = wireframe_info
                            st.session_state.analysis_complete = True
                            st.session_state.should_scroll = True
                            st.session_state.pdf_ready = False
                            st.session_state.pdf_bytes = None
                            
                            st.success("Analysis completed successfully! Thank you for your patience. Scroll down to see results.")
                            
                        except Exception as e:
                            st.error(f"Error during analysis: {str(e)}")
                            st.session_state.analysis_complete = False
            
            if 'analysis' in st.session_state:
                st.divider()
                
                st.markdown('<div id="analysis-results"></div>', unsafe_allow_html=True)
                
                analysis = st.session_state.analysis
                suggestions = st.session_state.suggestions
                wireframe_info = st.session_state.wireframe_info
                
                if st.session_state.get('should_scroll', False):
                    st.markdown("""
                    <script>
                        function scrollToResults() {
                            var element = document.getElementById('analysis-results');
                            if (element) {
                                // Add a small offset for better visibility
                                var offset = 80;
                                var elementPosition = element.getBoundingClientRect().top;
                                var offsetPosition = elementPosition + window.pageYOffset - offset;
                                
                                window.scrollTo({
                                    top: offsetPosition,
                                    behavior: 'smooth'
                                });
                                return true;
                            }
                            return false;
                        }
                        
                        // Wait for page to be fully loaded, then scroll
                        setTimeout(function() {
                            if (!scrollToResults()) {
                                // If element not found, retry with interval
                                var attempts = 0;
                                var interval = setInterval(function() {
                                    attempts++;
                                    if (scrollToResults() || attempts > 15) {
                                        clearInterval(interval);
                                    }
                                }, 300);
                            }
                        }, 500);
                    </script>
                    """, unsafe_allow_html=True)
                    st.session_state.should_scroll = False
                
                st.header("📊 Analysis Results")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    score = analysis['overall_score']
                    score_color = "green" if score > 0.7 else "orange" if score > 0.5 else "red"
                    st.metric("Overall Score", f"{score:.2f}/1.0", delta=None)
                    st.progress(score)
                
                with col2:
                    st.metric("Layout Type", analysis['layout']['layout_type'].title())
                
                with col3:
                    st.metric("Elements Detected", analysis['elements']['total_elements'])
                
                with col4:
                    st.metric("Unique Colors", analysis['colors']['unique_colors'])
                
                st.subheader("📈 Detailed Metrics")
                
                tab1, tab2, tab3, tab4 = st.tabs(["Layout", "Colors", "Spacing", "Wireframe"])
                
                with tab1:
                    layout = analysis['layout']
                    st.write(f"**Layout Type:** {layout['layout_type']}")
                    st.write(f"**Grid Score:** {layout['grid_score']:.2f}")
                    st.write(f"**Alignment Score:** {layout['alignment_score']:.2f}")
                    st.write(f"**Symmetry Score:** {layout['symmetry_score']:.2f}")
                
                with tab2:
                    colors = analysis['colors']
                    st.write(f"**Contrast Score:** {colors['contrast_score']:.2f}")
                    st.write(f"**Color Diversity:** {colors['color_diversity']:.2f}")
                    st.write("**Dominant Colors:**")
                    for i, color in enumerate(colors['dominant_colors'][:5], 1):
                        st.color_picker(f"Color {i}", f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}", disabled=True)
                
                with tab3:
                    spacing = analysis['spacing']
                    st.write(f"**Spacing Consistency:** {spacing['spacing_consistency']:.2f}")
                    st.write(f"**Whitespace Ratio:** {spacing['whitespace_ratio']:.2f}")
                    st.write(f"**Element Density:** {spacing['element_density']:.2f}")
                
                with tab4:
                    st.write("**Recommended Wireframe Structure:**")
                    structure = wireframe_info['structure']
                    for component, include in structure.items():
                        status = "Include" if include else "Optional"
                        st.write(f"- {component.title()}: {status}")
                    
                    st.write("\n**Recommendations:**")
                    for rec in wireframe_info['recommendations']:
                        st.write(f"- {rec}")
                
                st.divider()
                st.header("💡 Design Suggestions")
                
                high_priority = [s for s in suggestions if s['priority'] == 'high']
                medium_priority = [s for s in suggestions if s['priority'] == 'medium']
                low_priority = [s for s in suggestions if s['priority'] == 'low']
                
                if high_priority:
                    st.subheader("🔴 High Priority")
                    for suggestion in high_priority:
                        st.warning(f"**{suggestion['category'].replace('_', ' ').title()}:** {suggestion['message']}")
                
                if medium_priority:
                    st.subheader("🟡 Medium Priority")
                    for suggestion in medium_priority:
                        st.info(f"**{suggestion['category'].replace('_', ' ').title()}:** {suggestion['message']}")
                
                if low_priority:
                    st.subheader("🟢 Low Priority")
                    for suggestion in low_priority:
                        st.success(f"**{suggestion['category'].replace('_', ' ').title()}:** {suggestion['message']}")
                
                st.divider()
                st.subheader("📥 Download Reports")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    report = {
                        'analysis': analysis,
                        'suggestions': suggestions,
                        'wireframe_suggestions': wireframe_info
                    }
                    report_json = json.dumps(report, indent=2, default=str)
                    st.download_button(
                        label="📄 Download JSON Report",
                        data=report_json,
                        file_name="design_analysis_report.json",
                        mime="application/json"
                    )
                
                with col2:
                    if 'pdf_ready' not in st.session_state:
                        st.session_state.pdf_ready = False
                        st.session_state.pdf_bytes = None
                    
                    if st.button("Generate PDF Report", key="generate_pdf_btn"):
                        with st.spinner("Generating PDF report... Please wait"):
                            try:
                                st.session_state.pdf_bytes = st.session_state.pdf_generator.generate_pdf(report)
                                st.session_state.pdf_ready = True
                                st.success("PDF report ready for download!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error generating PDF: {str(e)}")
                                st.info("Please ensure reportlab is installed: pip install reportlab")
                                st.session_state.pdf_ready = False
                    
                    if st.session_state.pdf_ready and st.session_state.pdf_bytes:
                        st.download_button(
                            label="📑 Download PDF Report",
                            data=st.session_state.pdf_bytes,
                            file_name="design_analysis_report.pdf",
                            mime="application/pdf"
                        )

else:
    st.info("👆 Please upload an image to get started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### How to use:
        1. Upload a screenshot or wireframe of your UI/UX design
        2. Click "Analyze Design" to get AI-powered insights
        3. Review the analysis results and suggestions
        4. Download the full report if needed
        """)
    
    with col2:
        st.markdown("""
        ### What gets analyzed:
        - **Layout**: Grid structure, alignment, symmetry
        - **Colors**: Contrast, color diversity, dominant colors
        - **Spacing**: Consistency, whitespace, element density
        - **Elements**: Detection and positioning
        - **Wireframe**: Structure recommendations
        """)

