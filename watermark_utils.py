import cv2
import numpy as np

def get_contrasting_color(image, position = (50,50), font_scale=1, thickness=2):
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
    avg_color = np.mean(region, axis=(0,1))
    luminance = 0.299*avg_color[2] + 0.587*avg_color[1] + 0.114*avg_color[0]
    if luminance > 128:
        return (0, 0, 0)
    else:
        return (255, 255, 255)

def calculate_font_scale(image_width, text, font=cv2.FONT_HERSHEY_SIMPLEX, thickness=2, max_width_ratio=1.0):
    '''this calculates the scale of the font dynamically'''
    # Start with a base font scale
    font_scale = 1.0
    # Get the text width at base font scale
    (text_width, _), _ = cv2.getTextSize(text, font, font_scale, thickness)
    # Calculate the scale factor to fit the text within max_width_ratio * image_width
    scale_factor = (max_width_ratio * image_width) / text_width
    # Do not allow the text to be larger than the image
    if scale_factor > 1:
        scale_factor = 1
    return scale_factor

def add_transparent_text(image, text, font=cv2.FONT_HERSHEY_SIMPLEX, thickness=2, alpha=0.35, max_width_ratio=1.0):
    '''the function that adds the text to the image'''
    h, w = image.shape[:2]
    font_scale = calculate_font_scale(w, text, font, thickness, max_width_ratio)
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x = max(0, (w - text_width) // 2)
    y = (h + text_height) // 2
    position = (x, y)
    overlay = image.copy()
    color = get_contrasting_color(image, position, font_scale, thickness)
    cv2.putText(overlay, text, position, font, font_scale, color, thickness)
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
    return image
