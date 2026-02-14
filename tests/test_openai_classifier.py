import os
import io
import json
from PIL import Image

import pytest

import waste.waste_classifier as wc


class DummyOpenAI:
    @staticmethod
    def ChatCompletion_create(**kwargs):
        # Return a response object similar to openai.ChatCompletion.create
        class Choice:
            def __init__(self, content):
                self.message = {'content': content}

        # Provide JSON with non-normalized scores
        content = json.dumps({
            'biodegradable': 0.1,
            'plastic': 0.2,
            'ewaste': 0.4,
            'metal': 0.1,
            'glass': 0.15,
            'hazardous': 0.05
        })
        return {'choices': [{'message': {'content': content}}]}


def test_classify_with_openai_mock(monkeypatch):
    # Ensure module thinks openai is available
    monkeypatch.setattr(wc, 'OPENAI_AVAILABLE', True)
    monkeypatch.setenv('OPENAI_API_KEY', 'test')

    # Patch the openai object used in the module
    class Dummy:
        @staticmethod
        def ChatCompletion_create(**kwargs):
            return DummyOpenAI.ChatCompletion_create(**kwargs)

    # Create a fake openai with the expected call signatures
    dummy_openai = type('o', (), {
        'ChatCompletion': type('c', (), {'create': staticmethod(lambda **kw: DummyOpenAI.ChatCompletion_create(**kw))})
    })

    monkeypatch.setattr(wc, 'openai', dummy_openai, raising=False)

    # Initialize classifier (will set use_openai based on OPENAI_AVAILABLE and env var)
    classifier = wc.WasteClassifier()
    assert classifier.use_openai is True

    # Create a small test image
    img = Image.new('RGB', (200, 200), color='gray')

    scores = classifier._classify_with_openai(img)
    assert scores is not None
    # Check keys and normalization
    assert set(scores.keys()) == set(wc.WASTE_CATEGORIES.values())
    total = sum(scores.values())
    assert pytest.approx(total, rel=1e-3) == 1.0
