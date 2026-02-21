#!/usr/bin/env python
"""
Test script to verify plastic, metal, and glass waste classification
"""
import os
import django
import numpy as np
from PIL import Image
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings')
django.setup()

from waste.waste_classifier import WasteClassifier

def create_test_image(r, g, b, width=224, height=224):
    """Create a simple test image with specific RGB color"""
    img_array = np.full((height, width, 3), [r, g, b], dtype=np.uint8)
    return Image.fromarray(img_array, 'RGB')

def test_classification():
    """Test classifier with different waste types"""
    classifier = WasteClassifier()
    
    print("=" * 70)
    print("WASTE CLASSIFIER TEST - Plastic, Metal, Glass Detection")
    print("=" * 70)
    
    # Test cases
    tests = [
        ("PLASTIC (Blue)", 30, 144, 255),      # Blue plastic
        ("PLASTIC (White)", 255, 255, 255),    # White plastic bottle
        ("METAL (Silver)", 192, 192, 192),     # Silver metal
        ("METAL (Gray)", 128, 128, 128),       # Gray metal
        ("GLASS (Light Blue)", 173, 216, 230), # Light blue glass
        ("GLASS (Cyan)", 0, 255, 255),         # Cyan glass
    ]
    
    for test_name, r, g, b in tests:
        img = create_test_image(r, g, b)
        result = classifier.classify_image(img)
        
        print(f"\n{test_name} (RGB: {r}, {g}, {b})")
        print(f"  Detected: {result['category_display']}")
        print(f"  Confidence: {result['confidence']:.1%}")
        print(f"  All Scores:")
        for category, score in sorted(result['all_scores'].items(), key=lambda x: x[1], reverse=True):
            print(f"    - {category:15} : {score:.2%}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    test_classification()
