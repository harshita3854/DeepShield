# Install first:
#pip install icrawler

from icrawler.builtin import GoogleImageCrawler

# Number of images per class
NUM_IMAGES = 200

# -------- REAL IMAGES --------
real_crawler = GoogleImageCrawler(storage={'root_dir': 'dataset/real'})
real_crawler.crawl(
    keyword='real human face photo',
    max_num=NUM_IMAGES
)

# -------- FAKE / AI IMAGES --------
fake_crawler = GoogleImageCrawler(storage={'root_dir': 'dataset/fake'})
fake_crawler.crawl(
    keyword='AI generated human face',
    max_num=NUM_IMAGES
)

print("✅ Dataset download complete!")