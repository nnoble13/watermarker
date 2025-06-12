from watermark_utils import *
import os

text = '''sample only NOTFORSALE @asianobleart'''

for img in os.listdir('to_mark'):
    if img.endswith('.jpg') or img.endswith('.png'):
        image = cv2.imread(os.path.join('to_mark', img))
        image = add_transparent_text(image, text)
        cv2.imwrite(os.path.join('watermarked', img), image)
