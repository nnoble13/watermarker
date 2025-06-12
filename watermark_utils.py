import cv2
import numpy as np

def get_contrasting_color(image, position = (50,50), font_scale=1, thickness=2):
    '''this function should sample the image and then give back a contrasting color, ideally black or white'''
    x, y = position
    h, w, _ = image.shape
    x = min(max(x, 0), w-1)
    y = min(max(y, 0), h-1)
    sample_size = 10
    x_start = max(x - sample_size//2, 0)
    y_start = max(y - sample_size//2, 0)
    x_end = min(x + sample_size//2, w-1)
    y_end = min(y + sample_size//2, h-1)
    region = image[y_start:y_end, x_start:x_end]
    avg_color = np.mean(region, axis=(0,1)) #taking the mean of the area we're sampling
    luminance = 0.299*avg_color[2] + 0.587*avg_color[1] + 0.114*avg_color[0]
    if luminance > 128:
        return (0, 0, 0) # this is black, you can change the colors just use the diff codes for RGB between 0 to 255
    else:
        return (255, 255, 255)
def get_optimal_font_scale(text, width, font=cv2.FONT_HERSHEY_SIMPLEX, thickness=2):
    for scale in reversed(range(1, 100)):
        font_scale = scale / 10.0
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        if text_size[0] <= width:
            return font_scale
    return 1  # fallback

def add_transparent_text(image, text, font=cv2.FONT_HERSHEY_SIMPLEX, thickness=2, alpha=0.35):
    h, w = image.shape[:2]
    font_scale = get_optimal_font_scale(text, int(w * 0.98), font, thickness)  # 98% of width
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x = max(0, (w - text_width) // 2)
    y = (h + text_height) // 2
    position = (x, y)
    overlay = image.copy()
    color = get_contrasting_color(image, position, font_scale, thickness)
    cv2.putText(overlay, text, position, font, font_scale, color, thickness)
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
    return image
