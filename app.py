import streamlit as st
import cv2
import numpy as np
import zipfile
from PIL import Image
from io import BytesIO
from watermark_utils import add_transparent_text

st.title("Batch Image Watermarking Tool")

# Upload images
uploaded_files = st.file_uploader(
    "Upload images to watermark",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Watermark settings
watermark_text = st.text_input("Watermark text", "sample only NOTFORSALE @asianobleart")
alpha = st.slider("Text transparency", 0.0, 1.0, 0.35, 0.01)

# Initialize confirmation state
if "confirmed" not in st.session_state:
    st.session_state.confirmed = False

# Confirm button
if uploaded_files and not st.session_state.confirmed:
    st.info("Review your uploads and transparency setting, then click 'LFG' to proceed.")
    if st.button("LFG"):
        st.session_state.confirmed = True

# Process and download after confirmation
if st.session_state.confirmed:
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        with st.spinner("Processing images..."):
            for uploaded_file in uploaded_files:
                try:
                    pil_image = Image.open(uploaded_file).convert("RGB")
                    image = np.array(pil_image)
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    watermarked = add_transparent_text(
                        image,
                        watermark_text,
                        alpha=alpha
                    )
                    _, encoded_img = cv2.imencode(".png", watermarked)
                    img_bytes = encoded_img.tobytes()
                    zip_file.writestr(
                        f"watermarked_{uploaded_file.name}",
                        img_bytes
                    )
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")
    st.success("Processing complete! Ready for download.")
    st.download_button(
        label="⬇️ Download All Watermarked Images as ZIP",
        data=zip_buffer.getvalue(),
        file_name="watermarked_images.zip",
        mime="application/zip"
    )
    # Optionally, allow user to reset and start over
    if st.button("Start Over"):
        st.session_state.confirmed = False
