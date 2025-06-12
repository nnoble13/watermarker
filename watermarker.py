for img in os.listdir('to_mark'):
    if img.endswith('.jpg') or img.endswith('.png'):
        image = cv2.imread(os.path.join('to_mark', img))
        image = add_transparent_text(image, '''sample only NOTFORSALE @asianobleart''') #target_width_ratio=0.5)
        cv2.imwrite(os.path.join('watermarked', img), image)
