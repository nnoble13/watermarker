import cv2
import os
import numpy as np

def calculate_font_scale(image_width, text, font=cv2.FONT_HERSHEY_SIMPLEX, thickness=2, max_width_ratio=1.0):
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
