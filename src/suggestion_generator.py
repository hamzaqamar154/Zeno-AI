from typing import Dict, List
import random


class SuggestionGenerator:
    def __init__(self):
        self.improvement_templates = {
            'layout': [
                "Consider using a grid system to improve alignment and consistency",
                "The layout could benefit from better visual hierarchy",
                "Try grouping related elements together for better organization",
                "Consider adding more whitespace between major sections",
                "The current layout might benefit from a card-based design approach"
            ],
            'color_scheme': [
                "Consider using a more consistent color palette",
                "The contrast between text and background could be improved",
                "Try limiting your color palette to 3-5 primary colors",
                "Consider using color to establish visual hierarchy",
                "Ensure sufficient color contrast for accessibility (WCAG AA)"
            ],
            'typography': [
                "Consider establishing a clear typographic scale",
                "Text sizes could be more varied to create hierarchy",
                "Line spacing could be adjusted for better readability",
                "Consider using a maximum of 2-3 font families",
                "Ensure text is readable at different screen sizes"
            ],
            'spacing': [
                "Spacing between elements could be more consistent",
                "Consider using a spacing scale (4px, 8px, 16px, etc.)",
                "Add more whitespace to improve visual breathing room",
                "Group related elements with tighter spacing",
                "Ensure touch targets are at least 44x44 pixels"
            ],
            'accessibility': [
                "Ensure color contrast meets WCAG AA standards",
                "Add alt text for all images and icons",
                "Ensure interactive elements are keyboard accessible",
                "Consider users with color vision deficiencies",
                "Test with screen readers for proper navigation"
            ],
            'user_flow': [
                "Consider the user's journey through this screen",
                "Make primary actions more prominent",
                "Reduce cognitive load by simplifying choices",
                "Consider adding breadcrumbs or progress indicators",
                "Ensure error states are clearly communicated"
            ]
        }
        
        self.best_practices = [
            "Follow the 8-point grid system for consistent spacing",
            "Use F-pattern or Z-pattern layouts for better scanability",
            "Keep important content above the fold",
            "Ensure responsive design works on all screen sizes",
            "Use progressive disclosure to avoid overwhelming users",
            "Maintain consistent navigation patterns",
            "Provide clear feedback for user actions",
            "Use familiar UI patterns that users recognize"
        ]
    
    def generate_suggestions(self, analysis: Dict) -> List[Dict]:
        suggestions = []
        
        layout = analysis.get('layout', {})
        colors = analysis.get('colors', {})
        spacing = analysis.get('spacing', {})
        overall_score = analysis.get('overall_score', 0.5)
        
        if layout.get('grid_score', 0) < 0.5:
            suggestions.append({
                'type': 'improvement',
                'category': 'layout',
                'priority': 'high',
                'message': random.choice(self.improvement_templates['layout']),
                'score_impact': 0.15
            })
        
        if layout.get('alignment_score', 0) < 0.5:
            suggestions.append({
                'type': 'improvement',
                'category': 'layout',
                'priority': 'medium',
                'message': "Elements could be better aligned for a cleaner look",
                'score_impact': 0.1
            })
        
        if colors.get('contrast_score', 0) < 0.5:
            suggestions.append({
                'type': 'accessibility',
                'category': 'color_scheme',
                'priority': 'high',
                'message': random.choice(self.improvement_templates['color_scheme']),
                'score_impact': 0.2
            })
        
        if colors.get('color_diversity', 0) > 0.8:
            suggestions.append({
                'type': 'improvement',
                'category': 'color_scheme',
                'priority': 'medium',
                'message': "Consider reducing the number of colors for a more cohesive design",
                'score_impact': 0.1
            })
        
        if spacing.get('spacing_consistency', 0) < 0.6:
            suggestions.append({
                'type': 'improvement',
                'category': 'spacing',
                'priority': 'high',
                'message': random.choice(self.improvement_templates['spacing']),
                'score_impact': 0.15
            })
        
        if spacing.get('whitespace_ratio', 0) < 0.2:
            suggestions.append({
                'type': 'improvement',
                'category': 'spacing',
                'priority': 'medium',
                'message': "Adding more whitespace could improve readability and visual appeal",
                'score_impact': 0.1
            })
        
        if overall_score < 0.5:
            suggestions.append({
                'type': 'best_practice',
                'category': 'general',
                'priority': 'medium',
                'message': random.choice(self.best_practices),
                'score_impact': 0.1
            })
        
        if not suggestions:
            suggestions.append({
                'type': 'best_practice',
                'category': 'general',
                'priority': 'low',
                'message': "Design looks good! Consider A/B testing to optimize further",
                'score_impact': 0.05
            })
        
        suggestions.sort(key=lambda x: {'high': 3, 'medium': 2, 'low': 1}[x['priority']], reverse=True)
        
        return suggestions
    
    def generate_wireframe_suggestions(self, analysis: Dict) -> Dict:
        layout_type = analysis.get('layout', {}).get('layout_type', 'freeform')
        elements = analysis.get('elements', {}).get('total_elements', 0)
        
        wireframe_structure = {
            'header': True,
            'navigation': True,
            'main_content': True,
            'sidebar': elements > 10,
            'footer': True
        }
        
        recommendations = []
        
        if layout_type == 'grid-based':
            recommendations.append("Your design already follows a grid structure - maintain this in wireframes")
        elif layout_type == 'horizontal':
            recommendations.append("Consider a horizontal layout with clear sections")
        else:
            recommendations.append("A grid-based wireframe would help organize your content better")
        
        if elements > 15:
            recommendations.append("Consider breaking content into multiple screens or using tabs")
        
        return {
            'structure': wireframe_structure,
            'recommendations': recommendations,
            'layout_suggestion': layout_type
        }
    
    def format_suggestions(self, suggestions: List[Dict], use_emojis: bool = True) -> str:
        if not suggestions:
            return "No specific suggestions at this time."
        
        formatted = []
        for i, suggestion in enumerate(suggestions, 1):
            if use_emojis:
                priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[suggestion['priority']]
                formatted.append(
                    f"{i}. {priority_emoji} [{suggestion['priority'].upper()}] {suggestion['message']}"
                )
            else:
                priority_marker = {'high': '[HIGH]', 'medium': '[MEDIUM]', 'low': '[LOW]'}[suggestion['priority']]
                formatted.append(
                    f"{i}. {priority_marker} {suggestion['message']}"
                )
        
        return "\n".join(formatted)

