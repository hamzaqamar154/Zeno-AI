from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from typing import Dict, List
import io


class PDFReportGenerator:
    def __init__(self):
        pass
    
    def _get_styles(self):
        styles = getSampleStyleSheet()
        self._setup_custom_styles(styles)
        # Double-check that all required styles exist
        self._ensure_custom_styles(styles)
        return styles
    
    def _ensure_custom_styles(self, styles):
        """Force ensure all custom styles exist"""
        custom_styles = {
            'CustomTitle': {
                'parent': styles['Heading1'],
                'fontSize': 24,
                'textColor': colors.HexColor('#2c3e50'),
                'spaceAfter': 30,
                'alignment': TA_CENTER
            },
            'SectionHeader': {
                'parent': styles['Heading2'],
                'fontSize': 16,
                'textColor': colors.HexColor('#34495e'),
                'spaceAfter': 12,
                'spaceBefore': 20
            },
            'SubSection': {
                'parent': styles['Heading3'],
                'fontSize': 12,
                'textColor': colors.HexColor('#7f8c8d'),
                'spaceAfter': 8,
                'spaceBefore': 12
            },
            'BodyText': {
                'parent': styles['Normal'],
                'fontSize': 10,
                'spaceAfter': 6,
                'alignment': TA_JUSTIFY
            }
        }
        
        for name, style_params in custom_styles.items():
            if name not in styles.byName:
                style = ParagraphStyle(name=name, **style_params)
                try:
                    styles.add(style)
                except KeyError:
                    # If it already exists, that's fine
                    pass
    
    def _setup_custom_styles(self, styles):
        custom_styles = {
            'CustomTitle': {
                'parent': styles['Heading1'],
                'fontSize': 24,
                'textColor': colors.HexColor('#2c3e50'),
                'spaceAfter': 30,
                'alignment': TA_CENTER
            },
            'SectionHeader': {
                'parent': styles['Heading2'],
                'fontSize': 16,
                'textColor': colors.HexColor('#34495e'),
                'spaceAfter': 12,
                'spaceBefore': 20
            },
            'SubSection': {
                'parent': styles['Heading3'],
                'fontSize': 12,
                'textColor': colors.HexColor('#7f8c8d'),
                'spaceAfter': 8,
                'spaceBefore': 12
            },
            'BodyText': {
                'parent': styles['Normal'],
                'fontSize': 10,
                'spaceAfter': 6,
                'alignment': TA_JUSTIFY
            }
        }
        
        for name, style_params in custom_styles.items():
            # Check if style exists using byName dictionary
            if name not in styles.byName:
                style = ParagraphStyle(name=name, **style_params)
                try:
                    styles.add(style)
                except KeyError:
                    # Style might have been added by another thread/instance
                    # Verify it exists now
                    if name not in styles.byName:
                        raise
    
    def generate_pdf(self, report_data: Dict) -> bytes:
        styles = self._get_styles()
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        story.append(Paragraph("AI UX/UI Design Assistant", styles['CustomTitle']))
        story.append(Paragraph("Design Analysis Report", styles['SectionHeader']))
        story.append(Spacer(1, 0.2*inch))
        
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"<i>Generated on {report_date}</i>", styles['BodyText']))
        story.append(Spacer(1, 0.3*inch))
        
        analysis = report_data.get('analysis', {})
        suggestions = report_data.get('suggestions', [])
        wireframe_info = report_data.get('wireframe_suggestions', {})
        
        story.append(Paragraph("Executive Summary", styles['SectionHeader']))
        
        overall_score = analysis.get('overall_score', 0)
        score_text = self._get_score_description(overall_score)
        
        summary_data = [
            ['Overall Score', f"{overall_score:.2f}/1.0", score_text],
            ['Layout Type', analysis.get('layout', {}).get('layout_type', 'N/A').title(), ''],
            ['Elements Detected', str(analysis.get('elements', {}).get('total_elements', 0)), ''],
            ['Unique Colors', str(analysis.get('colors', {}).get('unique_colors', 0)), '']
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph("Detailed Analysis", styles['SectionHeader']))
        
        layout = analysis.get('layout', {})
        story.append(Paragraph("Layout Analysis", styles['SubSection']))
        layout_data = [
            ['Metric', 'Score'],
            ['Grid Score', f"{layout.get('grid_score', 0):.2f}"],
            ['Alignment Score', f"{layout.get('alignment_score', 0):.2f}"],
            ['Symmetry Score', f"{layout.get('symmetry_score', 0):.2f}"]
        ]
        layout_table = self._create_simple_table(layout_data)
        story.append(layout_table)
        story.append(Spacer(1, 0.2*inch))
        
        colors_data = analysis.get('colors', {})
        story.append(Paragraph("Color Analysis", styles['SubSection']))
        color_metrics = [
            ['Metric', 'Value'],
            ['Contrast Score', f"{colors_data.get('contrast_score', 0):.2f}"],
            ['Color Diversity', f"{colors_data.get('color_diversity', 0):.2f}"],
            ['Unique Colors', str(colors_data.get('unique_colors', 0))]
        ]
        color_table = self._create_simple_table(color_metrics)
        story.append(color_table)
        story.append(Spacer(1, 0.2*inch))
        
        spacing = analysis.get('spacing', {})
        story.append(Paragraph("Spacing Analysis", styles['SubSection']))
        spacing_metrics = [
            ['Metric', 'Value'],
            ['Spacing Consistency', f"{spacing.get('spacing_consistency', 0):.2f}"],
            ['Whitespace Ratio', f"{spacing.get('whitespace_ratio', 0):.2f}"],
            ['Element Density', f"{spacing.get('element_density', 0):.2f}"]
        ]
        spacing_table = self._create_simple_table(spacing_metrics)
        story.append(spacing_table)
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph("Design Suggestions", styles['SectionHeader']))
        
        if suggestions:
            high_priority = [s for s in suggestions if s.get('priority') == 'high']
            medium_priority = [s for s in suggestions if s.get('priority') == 'medium']
            low_priority = [s for s in suggestions if s.get('priority') == 'low']
            
            if high_priority:
                story.append(Paragraph("High Priority", styles['SubSection']))
                for i, suggestion in enumerate(high_priority, 1):
                    category = suggestion.get('category', 'general').replace('_', ' ').title()
                    message = suggestion.get('message', '')
                    story.append(Paragraph(f"<b>{i}. [{category}]</b> {message}", styles['BodyText']))
                    story.append(Spacer(1, 0.1*inch))
            
            if medium_priority:
                story.append(Paragraph("Medium Priority", styles['SubSection']))
                for i, suggestion in enumerate(medium_priority, 1):
                    category = suggestion.get('category', 'general').replace('_', ' ').title()
                    message = suggestion.get('message', '')
                    story.append(Paragraph(f"<b>{i}. [{category}]</b> {message}", styles['BodyText']))
                    story.append(Spacer(1, 0.1*inch))
            
            if low_priority:
                story.append(Paragraph("Low Priority", styles['SubSection']))
                for i, suggestion in enumerate(low_priority, 1):
                    category = suggestion.get('category', 'general').replace('_', ' ').title()
                    message = suggestion.get('message', '')
                    story.append(Paragraph(f"<b>{i}. [{category}]</b> {message}", styles['BodyText']))
                    story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph("No specific suggestions at this time.", styles['BodyText']))
        
        story.append(Spacer(1, 0.3*inch))
        
        if wireframe_info:
            story.append(Paragraph("Wireframe Recommendations", styles['SectionHeader']))
            
            structure = wireframe_info.get('structure', {})
            story.append(Paragraph("Recommended Structure", styles['SubSection']))
            structure_data = [['Component', 'Status']]
            for component, include in structure.items():
                status = "Include" if include else "Optional"
                structure_data.append([component.title().replace('_', ' '), status])
            
            structure_table = self._create_simple_table(structure_data)
            story.append(structure_table)
            story.append(Spacer(1, 0.2*inch))
            
            recommendations = wireframe_info.get('recommendations', [])
            if recommendations:
                story.append(Paragraph("Recommendations", styles['SubSection']))
                for i, rec in enumerate(recommendations, 1):
                    story.append(Paragraph(f"{i}. {rec}", styles['BodyText']))
                    story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("<i>Report generated by AI UX/UI Design Assistant</i>", 
                             ParagraphStyle(name='Footer', parent=styles['Normal'], 
                                          fontSize=8, alignment=TA_CENTER, 
                                          textColor=colors.grey)))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _create_simple_table(self, data):
        table = Table(data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        return table
    
    def _get_score_description(self, score):
        if score >= 0.8:
            return "Excellent"
        elif score >= 0.6:
            return "Good"
        elif score >= 0.4:
            return "Fair"
        else:
            return "Needs Improvement"

