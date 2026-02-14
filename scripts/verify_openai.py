#!/usr/bin/env python3
"""Simple local verification script for OpenAI integration with the waste classifier.

Usage:
  python scripts/verify_openai.py [path/to/image.jpg]

If no image path is given the script creates a small gray image and runs
classification. Requires `OPENAI_API_KEY` env var set and `openai` installed.
"""
import os
import sys
import io
import json
from PIL import Image

from waste.waste_classifier import WasteClassifier


def main():
    image_path = sys.argv[1] if len(sys.argv) > 1 else None

    if not os.getenv('OPENAI_API_KEY'):
        print('ERROR: OPENAI_API_KEY not set. Export it then retry.')
        sys.exit(2)

    # Prepare image
    if image_path:
        img = Image.open(image_path).convert('RGB')
    else:
        img = Image.new('RGB', (400, 400), color='gray')

    classifier = WasteClassifier()
    print('use_openai:', classifier.use_openai, 'use_ml:', classifier.use_ml)
    if not classifier.use_openai:
        print('OpenAI integration not active (missing package/key).')
        sys.exit(3)

    print('Running classification (this will call OpenAI and may incur costs)...')
    result = classifier.classify_image(img)

    print('\nResult:')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
