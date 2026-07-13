import os
import shutil
import random
from icrawler.builtin import BingImageCrawler

# Configuration
NUM_IMAGES = 200

# Directory paths
TEMP_REAL = 'dataset/temp_real'
TEMP_FAKE = 'dataset/temp_fake'

TRAIN_REAL = 'dataset/train/real'
TRAIN_FAKE = 'dataset/train/fake'
VAL_REAL = 'dataset/val/real'
VAL_FAKE = 'dataset/val/fake'

# Ensure directories exist
for path in [TEMP_REAL, TEMP_FAKE, TRAIN_REAL, TRAIN_FAKE, VAL_REAL, VAL_FAKE]:
    os.makedirs(path, exist_ok=True)

print("Starting download of Real face photos...")
real_crawler = BingImageCrawler(storage={'root_dir': TEMP_REAL})
real_crawler.crawl(
    keyword='real human face photo portrait',
    max_num=NUM_IMAGES
)

print("\nStarting download of Fake/AI face photos...")
fake_crawler = BingImageCrawler(storage={'root_dir': TEMP_FAKE})
fake_crawler.crawl(
    keyword='AI generated face portrait photo',
    max_num=NUM_IMAGES
)

def distribute_files(src_dir, train_dir, val_dir):
    files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]
    random.shuffle(files)
    
    # Relative split (80% train, 20% validation)
    split_idx = int(len(files) * 0.8)
    train_files = files[:split_idx]
    val_files = files[split_idx:]
    
    print(f"Distributing files from {src_dir}: {len(train_files)} to train, {len(val_files)} to val")
    
    for f in train_files:
        shutil.copy(os.path.join(src_dir, f), os.path.join(train_dir, f))
        
    for f in val_files:
        shutil.copy(os.path.join(src_dir, f), os.path.join(val_dir, f))

# Clean previous folders if they exist
for folder in [TRAIN_REAL, TRAIN_FAKE, VAL_REAL, VAL_FAKE]:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)

# Distribute images
distribute_files(TEMP_REAL, TRAIN_REAL, VAL_REAL)
distribute_files(TEMP_FAKE, TRAIN_FAKE, VAL_FAKE)

# Cleanup temp folders
print("\nCleaning up temporary download directories...")
shutil.rmtree(TEMP_REAL)
shutil.rmtree(TEMP_FAKE)

print("\n[OK] Dataset acquisition and partitioning complete!")
print(f"Train Real: {len(os.listdir(TRAIN_REAL))} images")
print(f"Train Fake: {len(os.listdir(TRAIN_FAKE))} images")
print(f"Val Real: {len(os.listdir(VAL_REAL))} images")
print(f"Val Fake: {len(os.listdir(VAL_FAKE))} images")
