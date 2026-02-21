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
                'colors': [(0, 0, 139), (30, 144, 255), (255, 192, 203), (0, 255, 127), (255, 255, 255), (192, 192, 192), (255, 0, 0), (0, 255, 0), (255, 255, 0)],  # Multiple colors
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
                'colors': [(192, 192, 192), (169, 169, 169), (211, 211, 211), (128, 128, 128), (255, 255, 255), (64, 64, 64), (224, 224, 224)],  # Gray, white, metallic colors
                'keywords': ['can', 'aluminum', 'steel', 'metal', 'shiny', 'reflective'],
                'texture': 'metallic',
                'shape': 'geometric'
            },
            'glass': {
                'colors': [(173, 216, 230), (240, 248, 255), (0, 255, 255), (255, 182, 193), (255, 255, 255), (200, 220, 240), (220, 240, 255), (192, 192, 192)],  # Light colors
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
        # By default avoid downloading ImageNet weights at runtime (may fail in restricted envs)
        use_imagenet = os.environ.get('WASTE_LOAD_IMAGENET', '0') == '1'
        weights_arg = 'imagenet' if use_imagenet else None

        try:
            self.models['mobilenet'] = MobileNetV2(weights=weights_arg, input_shape=(224, 224, 3))
            msg = "✓ MobileNetV2 model loaded"
            if not use_imagenet:
                msg += " (initialized without ImageNet weights)"
            print(msg)
        except Exception as e:
            print(f"Warning: Could not load MobileNetV2: {e}")

        try:
            self.models['resnet'] = ResNet50(weights=weights_arg, input_shape=(224, 224, 3))
            msg = "✓ ResNet50 model loaded"
            if not use_imagenet:
                msg += " (initialized without ImageNet weights)"
            print(msg)
        except Exception as e:
            print(f"Warning: Could not load ResNet50: {e}")

            # Attempt to load fine-tuned mobilenet weights (6-class classifier)
        try:
            weights_path = os.path.join('waste', 'model_weights', 'mobilenet_finetuned.weights.h5')
            class_idx_path = os.path.join('waste', 'model_weights', 'class_indices.json')
            if os.path.exists(weights_path) and TF_AVAILABLE:
                from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense
                from tensorflow.keras.models import Model
                # Instantiate base WITHOUT ImageNet weights to avoid downloads; we'll load finetuned weights next
                base = MobileNetV2(include_top=False, weights=None, input_shape=(224, 224, 3))
                x = base.output
                x = GlobalAveragePooling2D()(x)
                x = Dropout(0.3)(x)
                out = Dense(len(WASTE_CATEGORIES), activation='softmax', name='waste_output')(x)
                ft_model = Model(inputs=base.input, outputs=out)
                ft_model.load_weights(weights_path)
                self.models['mobilenet_finetuned'] = ft_model
                print("✓ Fine-tuned MobileNet weights loaded")

                # Load class index mapping if present
                if os.path.exists(class_idx_path):
                    try:
                        import json
                        with open(class_idx_path, 'r') as f:
                            class_indices = json.load(f)
                        # invert mapping to index -> class name
                        inv = {int(v): k for k, v in class_indices.items()}
                        self.class_index_map = inv
                    except Exception:
                        self.class_index_map = None
                else:
                    self.class_index_map = None
        except Exception as e:
            print(f"Warning: Could not load fine-tuned mobilenet weights: {e}")
    
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

            # Fine-tuned MobileNet (outputs waste-class probs)
            if 'mobilenet_finetuned' in self.models:
                mt_input = mobilenet_preprocess(img_array.copy())
                ft_preds = self.models['mobilenet_finetuned'].predict(mt_input, verbose=0)[0]
                # Map indices to category names
                if hasattr(self, 'class_index_map') and self.class_index_map:
                    ft_scores = {self.class_index_map[i]: float(ft_preds[i]) for i in range(len(ft_preds))}
                else:
                    classes = list(WASTE_CATEGORIES.values())
                    ft_scores = {classes[i]: float(ft_preds[i]) for i in range(len(ft_preds))}
                ensemble_scores['mobilenet_finetuned'] = ft_scores
            
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
        """Map ImageNet predictions to waste categories - EXPANDED"""
        # ImageNet class mappings for waste categories
        category_map = {
            'biodegradable': ['apple', 'orange', 'banana', 'cantaloupe', 'broccoli', 'cauliflower', 'corn', 'potato',
                             'acorn', 'artichoke', 'leaf', 'moss', 'hay', 'wood', 'straw', 'seaweed', 'carrot', 'lettuce',
                             'lemon', 'coconut', 'pumpkin', 'mushroom', 'pineapple', 'papaya', 'kiwi', 'avocado', 'peach'],
            'plastic': ['shopping_bag', 'plastic_bag', 'perfume', 'water_bottle', 'wine_bottle', 'bottle', 'plastic_bottle',
                       'cup', 'bowl', 'plate', 'carton', 'packet', 'box', 'toy', 'teddy_bear', 'doll', 'bucket', 'trash_can',
                       'container', 'sock', 'shoe', 'lampshade', 'desk', 'chair', 'backpack', 'suitcase'],
            'ewaste': ['computer', 'laptop', 'mobile_phone', 'telephone', 'monitor', 'keyboard', 'mouse', 'printer', 
                       'camera', 'speaker', 'headphones', 'circuit_board', 'remote', 'oscilloscope', 'microphone', 'switch',
                       'plug', 'extension_cord', 'power_strip', 'battery', 'projector', 'scanner'],
            'metal': ['can', 'aluminum_can', 'tin_can', 'bucket', 'kettle', 'pot', 'pan', 'fork', 'knife', 'spoon', 'wire', 
                     'chain', 'padlock', 'nail', 'screw', 'bolt', 'gate', 'fence', 'bell', 'gong', 'pipe', 'ladder', 'bicycle',
                     'motorcycle', 'car_mirror', 'trophy', 'cooking_pot'],
            'glass': ['glass', 'goblet', 'wine_glass', 'beer_glass', 'jar', 'vase', 'bottle', 'glass_bottle', 'drinking_glass',
                     'champagne_glass', 'margarita_glass', 'pitcher', 'bowl', 'eyeglasses', 'lens', 'mirror', 'aquarium',
                     'window', 'prism'],
            'hazardous': ['smoke', 'fire', 'flame', 'warning_sign', 'sign', 'caution', 'dangerous', 'toxic', 'skull', 'biohazard',
                         'radioactive', 'chemical', 'poison', 'explosion']
        }
        
        waste_scores = {cat: 0.0 for cat in WASTE_CATEGORIES.values()}
        
        # Get top predictions (increased for better detection)
        top_pred_indices = np.argsort(predictions)[-30:][::-1]
        
        for idx in top_pred_indices:
            pred_score = predictions[idx]
            # Map to waste categories
            for waste_cat, keywords in category_map.items():
                waste_cat_lower = waste_cat.lower()
                waste_scores[waste_cat_lower] = max(waste_scores[waste_cat_lower], pred_score * 0.7)
        
        # Normalize
        total = sum(waste_scores.values())
        if total > 0:
            waste_scores = {k: v/total for k, v in waste_scores.items()}
        else:
            waste_scores = {cat: 1/6 for cat in WASTE_CATEGORIES.values()}
        
        return waste_scores
    
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
                
                # Color matching (40% weight) - more lenient scoring
                color_dist = self._color_distance(features['dominant_color'], waste_info['colors'])
                color_score = 1.0 - min(color_dist / 350.0, 1.0)  # More lenient threshold
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
        """Color-based waste classification - IMPROVED"""
        try:
            img_array = np.array(img)
            
            # Get color histogram with more bins for better granularity
            hist_r = np.histogram(img_array[:, :, 0], bins=16, range=(0, 256))[0]
            hist_g = np.histogram(img_array[:, :, 1], bins=16, range=(0, 256))[0]
            hist_b = np.histogram(img_array[:, :, 2], bins=16, range=(0, 256))[0]
            
            # Normalize histograms
            hist_r = hist_r / (hist_r.sum() + 1e-8)
            hist_g = hist_g / (hist_g.sum() + 1e-8)
            hist_b = hist_b / (hist_b.sum() + 1e-8)
            
            # Calculate color statistics
            mean_r = np.mean(img_array[:, :, 0])
            mean_g = np.mean(img_array[:, :, 1])
            mean_b = np.mean(img_array[:, :, 2])
            
            scores = {}
            
            # Biodegradable: Green/Brown tones
            scores['biodegradable'] = (hist_g[5:12].sum() * 0.6 + hist_r[2:8].sum() * 0.3 + (1 - hist_b[8:16].sum()) * 0.1)
            
            # Plastic: Blue, Pink, Cyan, White - predominantly cool colors  
            scores['plastic'] = (hist_b[8:16].sum() * 0.5 + hist_g[6:14].sum() * 0.3 + (mean_b > mean_r) * 0.2)
            
            # E-waste: Dark colors (Gray, Black, Dark colors)
            scores['ewaste'] = ((1 - hist_g[6:16].mean() * 2) * 0.6 + (1 - hist_r[6:16].mean() * 2) * 0.4)
            
            # Metal: Bright grays, high contrast, similar R and G values (neutral tones)
            gray_similarity = 1.0 - (abs(mean_r - mean_g) / 256.0)
            scores['metal'] = (hist_r[10:16].sum() * 0.4 + gray_similarity * 0.5 + (mean_r > 100) * 0.1)
            
            # Glass: Bright, light colors (high brightness), blues and cyans
            brightness = (mean_r + mean_g + mean_b) / 3.0
            scores['glass'] = ((brightness / 255.0) * 0.5 + hist_b[10:16].sum() * 0.3 + hist_g[10:16].sum() * 0.2)
            
            # Hazardous: Red, Orange, Yellow tones
            scores['hazardous'] = (hist_r[10:16].sum() * 0.6 + (mean_r > mean_g) * 0.3 + (mean_r > mean_b) * 0.1)
            
            # Normalize
            total = sum(scores.values())
            if total > 0:
                scores = {k: v/total for k, v in scores.items()}
            else:
                scores = {cat: 1/6 for cat in WASTE_CATEGORIES.values()}
            
            return scores
        except Exception as e:
            print(f"Color classification error: {e}")
            return {cat: 1/6 for cat in WASTE_CATEGORIES.values()}
    
    def _ensemble_voting(self, scores_dict):
        """Combine multiple classification methods through weighted voting"""
        combined_scores = {cat: 0.0 for cat in WASTE_CATEGORIES.values()}
        
        # Weights for each method - IMPROVED for better plastic, metal, glass detection
        weights = {
            'neural_net': 0.35,  # 35% - Neural networks
            'features': 0.35,    # 35% - Advanced features (color, texture, brightness)
            'colors': 0.30       # 30% - Color analysis (IMPROVED algorithm)
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
