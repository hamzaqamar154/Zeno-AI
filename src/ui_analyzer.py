import cv2
import numpy as np
import os
from typing import Dict, List, Tuple
from pathlib import Path


class UIAnalyzer:
    def __init__(self):
        self.min_contour_area = 100
        
    def load_image(self, image_path: str) -> np.ndarray:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        return image
    
    def detect_elements(self, image: np.ndarray) -> Dict:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        elements = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                elements.append({
                    'bbox': (x, y, w, h),
                    'area': area,
                    'center': (x + w//2, y + h//2)
                })
        
        return {
            'total_elements': len(elements),
            'elements': elements,
            'image_dimensions': (image.shape[1], image.shape[0])
        }
    
    def analyze_layout(self, image: np.ndarray) -> Dict:
        height, width = image.shape[:2]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        horizontal_lines = self._detect_lines(gray, 'horizontal')
        vertical_lines = self._detect_lines(gray, 'vertical')
        
        grid_score = self._calculate_grid_score(horizontal_lines, vertical_lines, width, height)
        
        return {
            'layout_type': self._classify_layout(horizontal_lines, vertical_lines, grid_score),
            'grid_score': grid_score,
            'alignment_score': self._calculate_alignment_score(image),
            'symmetry_score': self._calculate_symmetry_score(image)
        }
    
    def _detect_lines(self, gray: np.ndarray, direction: str) -> List:
        if direction == 'horizontal':
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        else:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
        
        detected = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        lines = cv2.HoughLinesP(detected, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
        
        return lines.tolist() if lines is not None else []
    
    def _calculate_grid_score(self, h_lines: List, v_lines: List, width: int, height: int) -> float:
        if not h_lines or not v_lines:
            return 0.0
        
        h_count = len(h_lines)
        v_count = len(v_lines)
        total_pixels = width * height
        
        score = min((h_count + v_count) / 20.0, 1.0)
        return round(score, 2)
    
    def _classify_layout(self, h_lines: List, v_lines: List, grid_score: float) -> str:
        if grid_score > 0.7:
            return "grid-based"
        elif len(h_lines) > len(v_lines) * 2:
            return "horizontal"
        elif len(v_lines) > len(h_lines) * 2:
            return "vertical"
        else:
            return "freeform"
    
    def _calculate_alignment_score(self, image: np.ndarray) -> float:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=5)
        
        if lines is None or len(lines) < 3:
            return 0.3
        
        alignment_score = min(len(lines) / 30.0, 1.0)
        return round(alignment_score, 2)
    
    def _calculate_symmetry_score(self, image: np.ndarray) -> float:
        height, width = image.shape[:2]
        left_half = image[:, :width//2]
        right_half = cv2.flip(image[:, width//2:], 1)
        
        if left_half.shape != right_half.shape:
            right_half = cv2.resize(right_half, (left_half.shape[1], left_half.shape[0]))
        
        diff = cv2.absdiff(left_half, right_half)
        similarity = 1.0 - (np.mean(diff) / 255.0)
        
        return round(max(0.0, similarity), 2)
    
    def analyze_colors(self, image: np.ndarray) -> Dict:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pixels = image_rgb.reshape(-1, 3)
        
        unique_colors = np.unique(pixels, axis=0)
        dominant_colors = self._extract_dominant_colors(pixels, k=5)
        
        contrast_score = self._calculate_contrast_score(image_rgb)
        
        return {
            'unique_colors': len(unique_colors),
            'dominant_colors': dominant_colors,
            'contrast_score': contrast_score,
            'color_diversity': min(len(unique_colors) / 100.0, 1.0)
        }
    
    def _extract_dominant_colors(self, pixels: np.ndarray, k: int = 5) -> List[Tuple[int, int, int]]:
        try:
            from sklearn.cluster import KMeans
            
            sample_size = min(1000, len(pixels))
            sample = pixels[np.random.choice(len(pixels), sample_size, replace=False)]
            
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(sample)
            
            colors = kmeans.cluster_centers_.astype(int)
            return [tuple(color) for color in colors]
        except (ImportError, ValueError):
            # Fallback to simple histogram-based color extraction
            quantized = (pixels // 64) * 64
            unique_colors, counts = np.unique(quantized, axis=0, return_counts=True)
            top_indices = np.argsort(counts)[-k:][::-1]
            return [tuple(unique_colors[i]) for i in top_indices]
    
    def _calculate_contrast_score(self, image_rgb: np.ndarray) -> float:
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = hist.flatten()
        
        total_pixels = np.sum(hist)
        if total_pixels == 0:
            return 0.0
        
        hist_norm = hist / total_pixels
        
        mean = np.sum(np.arange(256) * hist_norm)
        std = np.sqrt(np.sum(((np.arange(256) - mean) ** 2) * hist_norm))
        
        contrast_score = min(std / 64.0, 1.0)
        return round(contrast_score, 2)
    
    def analyze_spacing(self, image: np.ndarray) -> Dict:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) < 2:
            return {
                'spacing_consistency': 0.5,
                'whitespace_ratio': 0.3,
                'element_density': 0.5
            }
        
        bounding_boxes = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > self.min_contour_area]
        
        if len(bounding_boxes) < 2:
            return {
                'spacing_consistency': 0.5,
                'whitespace_ratio': 0.3,
                'element_density': 0.5
            }
        
        distances = []
        for i, (x1, y1, w1, h1) in enumerate(bounding_boxes):
            for x2, y2, w2, h2 in bounding_boxes[i+1:]:
                center1 = (x1 + w1//2, y1 + h1//2)
                center2 = (x2 + w2//2, y2 + h2//2)
                dist = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
                distances.append(dist)
        
        if not distances:
            spacing_consistency = 0.5
        else:
            mean_dist = np.mean(distances)
            std_dist = np.std(distances)
            spacing_consistency = 1.0 - min(std_dist / mean_dist if mean_dist > 0 else 1.0, 1.0)
        
        total_area = image.shape[0] * image.shape[1]
        element_area = sum(w * h for _, _, w, h in bounding_boxes)
        whitespace_ratio = 1.0 - (element_area / total_area)
        
        element_density = len(bounding_boxes) / (total_area / 10000.0)
        element_density = min(element_density / 10.0, 1.0)
        
        return {
            'spacing_consistency': round(spacing_consistency, 2),
            'whitespace_ratio': round(whitespace_ratio, 2),
            'element_density': round(element_density, 2)
        }
    
    def full_analysis(self, image_path: str) -> Dict:
        image = self.load_image(image_path)
        
        elements = self.detect_elements(image)
        layout = self.analyze_layout(image)
        colors = self.analyze_colors(image)
        spacing = self.analyze_spacing(image)
        
        overall_score = (
            layout['grid_score'] * 0.3 +
            layout['alignment_score'] * 0.2 +
            colors['contrast_score'] * 0.2 +
            spacing['spacing_consistency'] * 0.15 +
            spacing['whitespace_ratio'] * 0.15
        )
        
        return {
            'image_path': image_path,
            'elements': elements,
            'layout': layout,
            'colors': colors,
            'spacing': spacing,
            'overall_score': round(overall_score, 2)
        }

