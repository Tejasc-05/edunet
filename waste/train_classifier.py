import os
import json
import argparse

try:
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
    from tensorflow.keras.models import Model
    from tensorflow.keras.optimizers import Adam
    TF_AVAILABLE = True
except Exception:
    TF_AVAILABLE = False

try:
    from waste.waste_classifier import WASTE_CATEGORIES
except Exception:
    # Fallback list if package imports fail (allows dry-run without full deps)
    WASTE_CATEGORIES = {0: 'biodegradable', 1: 'plastic', 2: 'ewaste', 3: 'metal', 4: 'glass', 5: 'hazardous'}


def build_model(num_classes, base_trainable=False, weights='imagenet'):
    weights_arg = weights if weights in ('imagenet', None) else 'imagenet'
    base = MobileNetV2(include_top=False, weights=weights_arg, input_shape=(224, 224, 3))
    base.trainable = base_trainable
    x = base.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.3)(x)
    out = Dense(num_classes, activation='softmax')(x)
    model = Model(inputs=base.input, outputs=out)
    model.compile(optimizer=Adam(1e-4), loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def train(dataset_dir, epochs=3, batch_size=16, dry_run=False, weights='imagenet'):
    if not TF_AVAILABLE:
        print('TensorFlow not available in this environment.')
        return

    classes = [v for v in WASTE_CATEGORIES.values()]
    num_classes = len(classes)

    if dry_run:
        print('Dry run: building model and saving initial weights...')
        model = build_model(num_classes, base_trainable=False, weights=weights if weights != 'none' else None)
        os.makedirs('waste/model_weights', exist_ok=True)
        model.save_weights('waste/model_weights/mobilenet_finetuned.weights.h5')
        with open('waste/model_weights/class_indices.json', 'w') as f:
            json.dump({c: i for i, c in enumerate(classes)}, f)
        print('Saved initial weights and class_indices.')
        return

    train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.15,
                                       rotation_range=20, horizontal_flip=True, zoom_range=0.2)

    train_gen = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        classes=classes,
        class_mode='categorical',
        subset='training'
    )

    val_gen = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        classes=classes,
        class_mode='categorical',
        subset='validation'
    )

    model = build_model(num_classes, base_trainable=False, weights=weights if weights != 'none' else None)

    # Short initial training
    model.fit(train_gen, validation_data=val_gen, epochs=epochs)

    os.makedirs('waste/model_weights', exist_ok=True)
    model.save_weights('waste/model_weights/mobilenet_finetuned.weights.h5')
    with open('waste/model_weights/class_indices.json', 'w') as f:
        json.dump(train_gen.class_indices, f)

    print('Training complete. Weights saved to waste/model_weights/mobilenet_finetuned.weights.h5')


def main():
    parser = argparse.ArgumentParser(description='Fine-tune waste classifier')
    parser.add_argument('--data', '-d', help='Path to dataset root (class subfolders)', default='data/train')
    parser.add_argument('--epochs', '-e', type=int, default=3)
    parser.add_argument('--batch', '-b', type=int, default=16)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--weights', choices=['imagenet','none'], default='imagenet', help='Use imagenet weights or none')
    args = parser.parse_args()

    train(args.data, epochs=args.epochs, batch_size=args.batch, dry_run=args.dry_run, weights=args.weights)


if __name__ == '__main__':
    main()
