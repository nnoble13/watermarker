import streamlit as st
import cv2
import numpy as np
import zipfile
from PIL import Image
from io import BytesIO
from watermark_utils import add_transparent_text

# Streamlit app configuration
st.set_page_config(page_title="Bulk Image Watermarker", layout="wide")
st.title("📸 Batch Image Watermarking Tool")

# File upload section
uploaded_files = st.file_uploader(
    "Upload images to watermark",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Watermark settings
watermark_text = st.text_input("Watermark text", "sample only NOTFORSALE @asianobleart")
alpha = st.slider("Text transparency", 0.0, 1.0, 0.35, 0.01)

if uploaded_files:
    # Create in-memory zip file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        with st.spinner("Processing images..."):
            for uploaded_file in uploaded_files:
                try:
                    # Convert uploaded file to OpenCV format
                    pil_image = Image.open(uploaded_file).convert("RGB")
                    image = np.array(pil_image)
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    # Apply watermark
                    watermarked = add_transparent_text(
                        image,
                        watermark_text,
                        alpha=alpha
                    )

                    # Convert back to bytes
                    _, encoded_img = cv2.imencode(".png", watermarked)
                    img_bytes = encoded_img.tobytes()

                    # Add to zip
                    zip_file.writestr(
                        f"watermarked_{uploaded_file.name}",
                        img_bytes
                    )

                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")

    # Show download button
    st.success("Processing complete! Ready for download.")
    st.download_button(
        label="⬇️ Download All Watermarked Images",
        data=zip_buffer.getvalue(),
        file_name="watermarked_images.zip",
        mime="application/zip"
    )
