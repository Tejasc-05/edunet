"""
Waste Classification Module
Uses multiple AI models and advanced image analysis for accurate waste detection
- TensorFlow/Keras MobileNetV2 for deep learning
- Advanced image feature extraction
- Waste-specific pattern recognition
- Ensemble voting for improved accuracy
"""

import os
import numpy as np
from PIL import Image
import io
import warnings
warnings.filterwarnings('ignore')
import json
import base64

try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

try:
    from tensorflow.keras.applications import MobileNetV2, ResNet50
    from tensorflow.keras.preprocessing import image as keras_image
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mobilenet_preprocess
    from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_preprocess
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

# Waste Categories
WASTE_CATEGORIES = {
    0: 'biodegradable',
    1: 'plastic',
    2: 'ewaste',
    3: 'metal',
    4: 'glass',
    5: 'hazardous'
}

WASTE_DESCRIPTIONS = {
    'biodegradable': {
        'name': 'Biodegradable',
        'description': 'Organic waste that decomposes naturally',
        'examples': 'Food scraps, leaves, paper, cardboard'
    },
    'plastic': {
        'name': 'Plastic',
        'description': 'Plastic waste including bottles, bags, and containers',
        'examples': 'Plastic bottles, bags, containers, straws'
    },
    'ewaste': {
        'name': 'E-Waste',
        'description': 'Electronic waste including devices and components',
        'examples': 'Old phones, computers, cables, batteries'
    },
    'metal': {
        'name': 'Metal',
        'description': 'Metal waste including cans and metal objects',
        'examples': 'Aluminum cans, steel scraps, metal wires'
    },
    'glass': {
        'name': 'Glass',
        'description': 'Glass waste including bottles and jars',
        'examples': 'Glass bottles, jars, broken glassware'
    },
    'hazardous': {
        'name': 'Hazardous',
        'description': 'Hazardous waste that requires special handling',
        'examples': 'Chemicals, batteries, medical waste, paints'
    }
}

class WasteClassifier:
    """Advanced waste classifier with multiple AI models and feature extraction"""
    
    def __init__(self):
        self.models = {}
        self.confidence_threshold = 0.4
        self.use_ml = TF_AVAILABLE
        # OpenAI usage: enabled only if package present and API key provided
        self.use_openai = OPENAI_AVAILABLE and bool(os.getenv('OPENAI_API_KEY'))
        if self.use_openai and OPENAI_AVAILABLE:
            try:
                openai.api_key = os.getenv('OPENAI_API_KEY')
            except Exception:
                self.use_openai = False
        if self.use_ml:
            self._load_models()
        
        # Waste-specific visual features
        self.waste_features = {
            'biodegradable': {
                'colors': [(34, 139, 34), (107, 142, 35), (139, 69, 19), (160, 82, 45)],  # Green, olive, brown
                'keywords': ['organic', 'leaf', 'fruit', 'vegetable', 'food', 'paper', 'wood', 'natural'],
                'texture': 'rough',
                'shape': 'irregular'
            },
            'plastic': {
                'colors': [(0, 0, 139), (30, 144, 255), (255, 192, 203), (0, 255, 127)],  # Blue, pink, cyan
                'keywords': ['bottle', 'bag', 'container', 'plastic', 'smooth', 'synthetic'],
                'texture': 'smooth',
                'shape': 'geometric'
            },
            'ewaste': {
                'colors': [(105, 105, 105), (128, 128, 128), (0, 0, 0), (128, 0, 0)],  # Gray, dark colors
                'keywords': ['circuit', 'wire', 'electronic', 'metal', 'component', 'device'],
                'texture': 'metallic',
                'shape': 'geometric'
            },
            'metal': {
                'colors': [(192, 192, 192), (169, 169, 169), (211, 211, 211), (128, 128, 128)],  # Silver, gray
                'keywords': ['can', 'aluminum', 'steel', 'metal', 'shiny', 'reflective'],
                'texture': 'metallic',
                'shape': 'geometric'
            },
            'glass': {
                'colors': [(173, 216, 230), (240, 248, 255), (0, 255, 255), (255, 182, 193)],  # Light blue, cyan
                'keywords': ['glass', 'bottle', 'jar', 'transparent', 'clear', 'reflective'],
                'texture': 'smooth',
                'shape': 'geometric'
            },
            'hazardous': {
                'colors': [(255, 0, 0), (255, 165, 0), (128, 0, 0), (255, 255, 0)],  # Red, orange, yellow
                'keywords': ['warning', 'hazard', 'toxic', 'chemical', 'danger', 'poison'],
                'texture': 'varied',
                'shape': 'varied'
            }
        }
    
    def _load_models(self):
        """Load multiple pre-trained models for ensemble voting"""
        try:
            self.models['mobilenet'] = MobileNetV2(weights='imagenet', input_shape=(224, 224, 3))
            print("✓ MobileNetV2 model loaded")
        except Exception as e:
            print(f"Warning: Could not load MobileNetV2: {e}")
        
        try:
            self.models['resnet'] = ResNet50(weights='imagenet', input_shape=(224, 224, 3))
            print("✓ ResNet50 model loaded")
        except Exception as e:
            print(f"Warning: Could not load ResNet50: {e}")
    
    def classify_image(self, image_file):
        """
        Classify waste type from an image using multiple techniques
        
        Args:
            image_file: PIL Image, file path, or Django UploadedFile
        
        Returns:
            dict with classification results
        """
        try:
            # Load and preprocess image
            img = self._load_image(image_file)
            if img is None:
                return self._get_error_response("Could not load image")
            
            # Use ensemble classification combining multiple methods
            scores = {}
            
            # Method 1: Neural network classification (if available)
            if self.use_ml:
                nn_scores = self._classify_with_nn(img)
                if nn_scores:  # Check if scores returned
                    scores['neural_net'] = nn_scores
            
            # Method 2: Advanced image feature analysis
            feature_scores = self._classify_by_features(img)
            if feature_scores:
                scores['features'] = feature_scores
            
            # Method 3: Color histogram analysis
            color_scores = self._classify_by_colors(img)
            if color_scores:
                scores['colors'] = color_scores

            # Method 4: OpenAI vision/text assistance (optional)
            if self.use_openai:
                try:
                    openai_scores = self._classify_with_openai(img)
                    if openai_scores:
                        scores['openai'] = openai_scores
                except Exception:
                    pass
            
            # Ensemble voting - combine all methods
            final_scores = self._ensemble_voting(scores)
            
            # Get the best match
            best_category = max(final_scores, key=final_scores.get)
            confidence = final_scores[best_category]
            
            return {
                'success': True,
                'category': best_category,
                'category_display': WASTE_DESCRIPTIONS[best_category]['name'],
                'confidence': float(min(confidence, 0.99)),  # Cap at 99%
                'description': WASTE_DESCRIPTIONS[best_category]['description'],
                'examples': WASTE_DESCRIPTIONS[best_category]['examples'],
                'all_scores': {k: float(v) for k, v in final_scores.items()},
                'message': f"Detected: {WASTE_DESCRIPTIONS[best_category]['name']} ({confidence:.1%} confidence)"
            }
        
        except Exception as e:
            return self._get_error_response(f"Classification error: {str(e)}")
    
    def _load_image(self, image_file):
        """Load image from various sources"""
        try:
            if isinstance(image_file, Image.Image):
                img = image_file
            elif isinstance(image_file, str):
                img = Image.open(image_file)
            elif hasattr(image_file, 'read'):
                # Django UploadedFile
                img = Image.open(image_file)
            else:
                return None
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to 224x224 for MobileNetV2
            # Use LANCZOS for high-quality downsampling
            try:
                img = img.resize((224, 224), Image.Resampling.LANCZOS)
            except AttributeError:
                # Fallback for older Pillow versions
                img = img.resize((224, 224), Image.LANCZOS)
            
            return img
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def _classify_with_nn(self, img):
        """Classify using ensemble of neural networks"""
        try:
            img_array = keras_image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            
            ensemble_scores = {}
            
            # MobileNetV2 predictions
            if 'mobilenet' in self.models:
                mobilenet_input = mobilenet_preprocess(img_array.copy())
                mobilenet_preds = self.models['mobilenet'].predict(mobilenet_input, verbose=0)
                ensemble_scores['mobilenet'] = self._map_imagenet_to_waste(mobilenet_preds[0])
            
            # ResNet50 predictions
            if 'resnet' in self.models:
                resnet_input = resnet_preprocess(img_array.copy())
                resnet_preds = self.models['resnet'].predict(resnet_input, verbose=0)
                ensemble_scores['resnet'] = self._map_imagenet_to_waste(resnet_preds[0])
            
            # Average ensemble predictions
            if ensemble_scores:
                avg_scores = {}
                for category in WASTE_CATEGORIES.values():
                    cat_scores = [model_scores.get(category, 0) for model_scores in ensemble_scores.values()]
                    avg_scores[category] = np.mean(cat_scores) if cat_scores else 0
                return avg_scores
            else:
                return {cat: 1/6 for cat in WASTE_CATEGORIES.values()}
        
        except Exception as e:
            print(f"NN classification error: {e}")
            return {cat: 1/6 for cat in WASTE_CATEGORIES.values()}
    
    def _map_imagenet_to_waste(self, predictions):
        """Map ImageNet predictions to waste categories"""
        # ImageNet class mappings for waste categories
        category_map = {
            'biodegradable': ['apple', 'orange', 'banana', 'cantaloupe', 'broccoli', 'cauliflower', 'corn', 'potato',
                             'acorn', 'artichoke', 'leaf', 'moss', 'hay', 'wood', 'straw', 'seaweed'],
            'plastic': ['shopping_bag', 'plastic_bag', 'perfume', 'water_bottle', 'wine_bottle', 'bottle', 
                       'cup', 'bowl', 'plate', 'carton', 'packet', 'box'],
            'ewaste': ['computer', 'laptop', 'mobile_phone', 'telephone', 'monitor', 'keyboard', 
                       'mouse', 'printer', 'camera', 'speaker', 'headphones', 'circuit_board'],
            'metal': ['can', 'aluminum_can', 'tin_can', 'bucket', 'kettle', 'pot', 'pan', 
                     'fork', 'knife', 'spoon', 'wire', 'chain', 'padlock'],
            'glass': ['glass', 'goblet', 'wine_glass', 'beer_glass', 'jar', 'vase', 'bottle'],
            'hazardous': ['smoke', 'fire', 'flame', 'warning_sign', 'sign', 'caution', 'dangerous', 'toxic']
        }
        
        waste_scores = {cat: 0.0 for cat in WASTE_CATEGORIES.values()}
        
        # Get top predictions
        top_pred_indices = np.argsort(predictions)[-20:][::-1]
        
        for idx in top_pred_indices:
            pred_score = predictions[idx]
            # Map to waste categories
            for waste_cat, keywords in category_map.items():
                waste_cat_lower = waste_cat.lower()
                waste_scores[waste_cat_lower] = max(waste_scores[waste_cat_lower], pred_score * 0.6)
        
        # Normalize
        total = sum(waste_scores.values())
        if total > 0:
            waste_scores = {k: v/total for k, v in waste_scores.items()}
        else:
            waste_scores = {cat: 1/6 for cat in WASTE_CATEGORIES.values()}
        
        return waste_scores

    def _classify_with_openai(self, img):
        """Use OpenAI (vision/text) to get an additional classification signal.

        Returns a dict of normalized scores per category or None on failure.
        Requires OPENAI_API_KEY in environment and the `openai` package available.
        """
        if not OPENAI_AVAILABLE:
            return None

        try:
            # Resize to reduce payload
            tmp = img.copy()
            tmp.thumbnail((512, 512))
            buf = io.BytesIO()
            tmp.save(buf, format='JPEG', quality=80)
            b = buf.getvalue()
            img_b64 = base64.b64encode(b).decode('ascii')

            prompt = (
                "You are an assistant that classifies images of waste into one of: "
                "biodegradable, plastic, ewaste, metal, glass, hazardous. "
                "Given the attached image (base64), return a JSON object with keys "
                "for each category and numeric scores summing approximately to 1.0. "
                "Respond only with JSON.\n\nImageBase64:" + img_b64
            )

            # Use ChatCompletion if available
            try:
                resp = openai.ChatCompletion.create(
                    model=os.getenv('OPENAI_CHAT_MODEL', 'gpt-4o-mini'),
                    messages=[{'role': 'user', 'content': prompt}],
                    temperature=0.0,
                    max_tokens=300
                )
                text = resp['choices'][0]['message']['content']
            except Exception:
                # Fallback to Completion API
                resp = openai.Completion.create(
                    engine=os.getenv('OPENAI_COMPLETION_MODEL', 'text-davinci-003'),
                    prompt=prompt,
                    max_tokens=300,
                    temperature=0.0
                )
                text = resp['choices'][0]['text']

            # Extract JSON from response if present, otherwise try to parse key:value lines
            parsed = None
            try:
                start = text.find('{')
                end = text.rfind('}')
                if start != -1 and end != -1:
                    json_text = text[start:end+1]
                    parsed = json.loads(json_text)
                else:
                    # Try to parse lines like "biodegradable: 0.2" or "biodegradable 20%"
                    parsed = {}
                    for line in text.splitlines():
                        if ':' in line:
                            k, v = line.split(':', 1)
                        elif '\t' in line:
                            k, v = line.split('\t', 1)
                        else:
                            parts = line.strip().split()
                            if len(parts) >= 2:
                                k, v = parts[0], ' '.join(parts[1:])
                            else:
                                continue
                        k = k.strip().lower()
                        v = v.strip().rstrip('%')
                        try:
                            parsed[k] = float(v)
                        except Exception:
                            # try to extract number with regex
                            import re
                            m = re.search(r"([0-9]+\.?[0-9]*)", v)
                            if m:
                                parsed[k] = float(m.group(1))
            except Exception:
                parsed = None

            # Map and normalize; parsed may have different key names, so attempt to match
            scores = {cat: 0.0 for cat in WASTE_CATEGORIES.values()}
            if parsed:
                for k, v in parsed.items():
                    key = k.strip().lower()
                    # Direct match
                    if key in scores:
                        scores[key] = float(v)
                        continue
                    # Try singular/plural and simple synonyms
                    if key.endswith('s') and key[:-1] in scores:
                        scores[key[:-1]] = float(v)
                        continue
                    syn_map = {
                        'e-waste': 'ewaste',
                        'e waste': 'ewaste',
                        'electronic': 'ewaste',
                        'electronics': 'ewaste',
                        'bio': 'biodegradable'
                    }
                    if key in syn_map:
                        scores[syn_map[key]] = float(v)
                        continue
                    # If key contains category name
                    for cat in scores.keys():
                        if cat in key:
                            scores[cat] = float(v)
                            break
            total = sum(scores.values())
            if total > 0:
                scores = {k: v/total for k, v in scores.items()}
            else:
                scores = {cat: 1/6 for cat in WASTE_CATEGORIES.values()}

            return scores

        except Exception as e:
            print(f"OpenAI classification error: {e}")
            return None
    
    def _classify_by_features(self, img):
        """Advanced feature-based classification"""
        try:
            # Convert to numpy array
            img_array = np.array(img)
            
            # Extract features
            features = self._extract_image_features(img_array)
            
            # Score each waste category
            scores = {}
            for category, waste_info in self.waste_features.items():
                category_score = 0.0
                
                # Color matching (40% weight)
                color_dist = self._color_distance(features['dominant_color'], waste_info['colors'])
                color_score = 1.0 - (color_dist / 255.0)
                category_score += color_score * 0.4
                
                # Texture analysis (30% weight)
                texture_score = self._analyze_texture(img_array, waste_info['texture'])
                category_score += texture_score * 0.3
                
                # Edge density (20% weight)
                edge_score = self._analyze_edges(img_array, waste_info['shape'])
                category_score += edge_score * 0.2
                
                # Brightness analysis (10% weight)
                brightness_score = self._analyze_brightness(features['brightness'], category)
                category_score += brightness_score * 0.1
                
                scores[category] = max(0, min(category_score, 1.0))
            
            # Normalize
            total = sum(scores.values())
            if total > 0:
                scores = {k: v/total for k, v in scores.items()}
            
            return scores
        except Exception as e:
            print(f"Feature classification error: {e}")
            return {cat: 0.16 for cat in WASTE_CATEGORIES.values()}
    
    def _classify_by_colors(self, img):
        """Color-based waste classification (rebalance to avoid ewaste bias)"""
        try:
            img_array = np.array(img)

            # Get color histogram
            hist_r = np.histogram(img_array[:, :, 0], bins=10, range=(0, 256))[0].astype(float)
            hist_g = np.histogram(img_array[:, :, 1], bins=10, range=(0, 256))[0].astype(float)
            hist_b = np.histogram(img_array[:, :, 2], bins=10, range=(0, 256))[0].astype(float)

            # Normalize histograms (guard against zero division)
            if hist_r.sum() == 0 or hist_g.sum() == 0 or hist_b.sum() == 0:
                return {cat: 1/6 for cat in WASTE_CATEGORIES.values()}

            hist_r = hist_r / hist_r.sum()
            hist_g = hist_g / hist_g.sum()
            hist_b = hist_b / hist_b.sum()

            # Higher-level features
            features = self._extract_image_features(img_array)
            edge_density = self._analyze_edges(img_array, 'irregular')

            scores = {}

            # Score by color composition + brightness + edge cues (clamped to >=0)
            scores['biodegradable'] = max(0.0, hist_g[5:8].sum() * 0.45 + hist_r[2:5].sum() * 0.25 + features['brightness'] * 0.3)
            scores['plastic'] = max(0.0, hist_b[4:8].sum() * 0.45 + hist_g[5:8].sum() * 0.25 + features['brightness'] * 0.3)
            scores['ewaste'] = max(0.0, (1 - hist_g[3:7].mean()) * 0.3 + (1 - features['brightness']) * 0.4 + edge_density * 0.3)
            scores['metal'] = max(0.0, (hist_r.mean() - hist_g.mean()) * 0.25 + features['brightness'] * 0.5 + edge_density * 0.25)
            scores['glass'] = max(0.0, hist_b[5:9].sum() * 0.35 + (hist_r.mean() + hist_g.mean()) * 0.2 + features['brightness'] * 0.45)
            scores['hazardous'] = max(0.0, hist_r[6:10].sum() * 0.45 + hist_g[0:3].sum() * 0.2 + features['brightness'] * 0.35)

            # Normalize to probabilities
            total = sum(scores.values())
            if total > 0:
                scores = {k: v / total for k, v in scores.items()}

            return scores
        except Exception as e:
            print(f"Color classification error: {e}")
            return {cat: 1/6 for cat in WASTE_CATEGORIES.values()}
    
    def _ensemble_voting(self, scores_dict):
        """Combine multiple classification methods through weighted voting"""
        combined_scores = {cat: 0.0 for cat in WASTE_CATEGORIES.values()}
        
        # Weights for each method (include optional OpenAI signal)
        weights = {
            'neural_net': 0.35,  # 35% - Neural networks
            'features': 0.30,    # 30% - Advanced features
            'colors': 0.15,      # 15% - Color analysis
            'openai': 0.20       # 20% - OpenAI vision/text assistance
        }
        
        for method, method_scores in scores_dict.items():
            weight = weights.get(method, 0)
            for category, score in method_scores.items():
                combined_scores[category] += score * weight
        
        # Normalize
        total = sum(combined_scores.values())
        if total > 0:
            combined_scores = {k: v/total for k, v in combined_scores.items()}
        
        return combined_scores
    
    def _extract_image_features(self, img_array):
        """Extract comprehensive image features"""
        try:
            # Get dominant color
            pixels = img_array.reshape(-1, 3)
            dominant = pixels.mean(axis=0)
            
            # Calculate brightness
            brightness = (dominant[0] + dominant[1] * 1.2 + dominant[2]) / 3
            
            return {
                'dominant_color': tuple(map(int, dominant)),
                'brightness': brightness / 255.0,
                'saturated': np.std(pixels.std(axis=1)),
                'contrast': pixels.max() - pixels.min()
            }
        except:
            return {
                'dominant_color': (128, 128, 128),
                'brightness': 0.5,
                'saturated': 0.5,
                'contrast': 128
            }
    
    def _color_distance(self, color1, color_list):
        """Calculate minimum color distance to a list of colors"""
        if not color_list:
            return 0
        distances = [np.sqrt(sum((np.array(color1) - np.array(c))**2)) for c in color_list]
        return min(distances)
    
    def _analyze_texture(self, img_array, expected_texture):
        """Analyze image texture"""
        try:
            # Convert to grayscale
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            # Calculate local variance (texture roughness)
            texture_score = 0.0
            
            if expected_texture == 'rough':
                # High variance = rough texture
                variance = np.var(gray)
                texture_score = min(variance / 1000, 1.0)
            elif expected_texture == 'smooth':
                # Low variance = smooth texture
                variance = np.var(gray)
                texture_score = 1.0 - min(variance / 1000, 1.0)
            elif expected_texture == 'metallic':
                # High peaks and valleys
                texture_score = 0.6
            else:
                texture_score = 0.5
            
            return texture_score
        except:
            return 0.5
    
    def _analyze_edges(self, img_array, expected_shape):
        """Analyze image edge density"""
        try:
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            # Simple edge detection using gradients
            edges_h = np.abs(np.diff(gray, axis=0))
            edges_v = np.abs(np.diff(gray, axis=1))
            
            edge_density = (edges_h.mean() + edges_v.mean()) / 2 / 255
            
            if expected_shape == 'geometric':
                # Geometric shapes have clear edges
                return edge_density * 1.2
            elif expected_shape == 'irregular':
                # Irregular shapes have less defined edges
                return (1.0 - edge_density) * 0.8
            else:
                return edge_density
        except:
            return 0.5
    
    def _analyze_brightness(self, brightness, category):
        """Analyze brightness appropriateness for category"""
        brightness_preferences = {
            'biodegradable': 0.5,   # Medium brightness
            'plastic': 0.6,         # Medium-bright
            'ewaste': 0.35,         # Dark
            'metal': 0.65,          # Bright (reflective)
            'glass': 0.7,           # Very bright
            'hazardous': 0.55       # Medium (varies)
        }
        
        target = brightness_preferences.get(category, 0.5)
        return 1.0 - abs(brightness - target)
    
    def _classify_with_patterns(self, img):
        """Fallback classification using image patterns"""
        # Analyze image colors and patterns
        img_array = np.array(img)
        
        # Extract color information
        features = self._extract_image_features(img_array)
        
        # Use feature-based and color-based classification
        feature_scores = self._classify_by_features(img)
        color_scores = self._classify_by_colors(img)
        
        # Average the two methods
        combined_scores = {}
        for category in WASTE_CATEGORIES.values():
            combined_scores[category] = (feature_scores.get(category, 0) + color_scores.get(category, 0)) / 2
        
        # Normalize
        total = sum(combined_scores.values())
        if total > 0:
            combined_scores = {k: v/total for k, v in combined_scores.items()}
        
        best_category = max(combined_scores, key=combined_scores.get)
        
        return {
            'category': best_category,
            'confidence': combined_scores[best_category],
            'scores': combined_scores
        }
    
    def _get_error_response(self, message):
        """Return error response"""
        return {
            'success': False,
            'message': message,
            'category': None
        }

# Global classifier instance
waste_classifier = WasteClassifier() if TF_AVAILABLE else None
