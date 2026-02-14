#!/usr/bin/env python
"""
Test script for the waste classifier image resizing fix
"""
import os
import sys
import django
from PIL import Image
import io

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings')
django.setup()

from waste.waste_classifier import WasteClassifier

def test_image_resizing():
    """Test that images are properly resized before classification"""
    print("=" * 60)
    print("Testing Waste Classifier - Image Resizing Fix")
    print("=" * 60)
    
    # Create a test image at the problematic size (480, 640, 3)
    print("\n1. Creating test image (480x640)...")
    test_img = Image.new('RGB', (480, 640), color='green')
    print(f"   ✓ Test image created: {test_img.size}")
    
    # Save to bytes
    img_bytes = io.BytesIO()
    test_img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Load and test classifier
    print("\n2. Initializing WasteClassifier...")
    classifier = WasteClassifier()
    print(f"   ✓ Classifier initialized (TensorFlow available: {classifier.use_ml})")
    
    # Test classification
    print("\n3. Testing image classification...")
    try:
        result = classifier.classify_image(img_bytes)
        
        if result['success']:
            print(f"   ✓ Classification successful!")
            print(f"     - Category: {result['category_display']}")
            print(f"     - Confidence: {result['confidence']:.1%}")
            print(f"     - Description: {result['description']}")
        else:
            print(f"   ✗ Classification failed: {result['message']}")
            return False
    except Exception as e:
        print(f"   ✗ Error during classification: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    return True

def test_classifier_with_bytes():
    """Test classifier with BytesIO object (as used by Django)"""
    print("\n" + "=" * 60)
    print("Testing with BytesIO (Django Upload Format)")
    print("=" * 60)
    
    # Create different sized test images
    test_sizes = [(480, 640), (640, 480), (1024, 768), (300, 300)]
    
    classifier = WasteClassifier()
    
    for width, height in test_sizes:
        print(f"\n  Testing image size: {width}x{height}")
        
        test_img = Image.new('RGB', (width, height), color='blue')
        img_bytes = io.BytesIO()
        test_img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        try:
            result = classifier.classify_image(img_bytes)
            if result['success']:
                print(f"    ✓ Success: {result['category_display']} ({result['confidence']:.0%})")
            else:
                print(f"    ✗ Failed: {result['message']}")
        except Exception as e:
            print(f"    ✗ Error: {str(e)[:60]}...")
    
    print("\n" + "=" * 60)
    print("✓ BytesIO tests completed!")
    print("=" * 60)

if __name__ == '__main__':
    success = test_image_resizing()
    if success:
        test_classifier_with_bytes()
    
    sys.exit(0 if success else 1)
