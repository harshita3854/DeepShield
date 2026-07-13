import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ==========================================
# DeepShield - CNN Training Script
# ==========================================

# Define model parameters
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32
EPOCHS = 10

def build_model():
    """Builds a simple CNN architecture for binary classification (Real vs Fake)."""
    model = models.Sequential([
        layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        
        # Classification head
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5), # Prevent overfitting
        layers.Dense(1, activation='sigmoid') # Sigmoid for binary classification
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

def train_model(train_dir, val_dir, model_save_path):
    """Trains the CNN on the provided dataset directories."""
    print("Initializing Data Generators...")
    
    # Preprocessing & Data Augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    model = build_model()
    model.summary()
    
    print("\nStarting Training...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator
    )
    
    print(f"\nTraining Complete. Saving model to {model_save_path}")
    model.save(model_save_path)
    print("Model saved successfully!")

if __name__ == "__main__":
    # Example paths - User needs to specify actual dataset paths
    TRAIN_DIR = "dataset/train"
    VAL_DIR = "dataset/val"
    MODEL_PATH = "models_store/deepfake_detector_model.h5"
    
    if os.path.exists(TRAIN_DIR) and os.path.exists(VAL_DIR):
        train_model(TRAIN_DIR, VAL_DIR, MODEL_PATH)
    else:
        print("Note: Dataset directories not found.")
        print("Please place your training data (e.g. Real/Fake subfolders) in 'dataset/train' and 'dataset/val'.")
        print("Model architecture is ready to compile and run.")
