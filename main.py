import cv2
import streamlit as st
import numpy as np

from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO


def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def generate_output(image):
    image_w_barcodes, detected_barcodes = get_barcodes(image)
    col1.write("Original Image:")
    col1.image(image_w_barcodes)

    col2.write("Parsed barcodes:")
    st.sidebar.markdown("\n")
    col2.write(detected_barcodes)


def get_barcodes(image_loaded):
    img = np.array(image_loaded)
    print(image_loaded)
    detected_barcodes = decode(image_loaded)

    # If not detected then print the message
    if not detected_barcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
    else:
        # Traverse through all the detected barcodes in image
        for idx, barcode in enumerate(reversed(detected_barcodes)):
            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect

            # Put the rectangle in image using
            # cv2 to highlight the barcode
            cv2.rectangle(
                img, (x - 10, y - 10),
                (x + w + 10, y + h + 10),
                (255, 0, 0),
                2,
            )

            if barcode.data != "":
                print(idx + 1, str(barcode.data))

    barcodes_values = [i[0] for i in detected_barcodes]

    return img, barcodes_values


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Barcode reader")

    st.sidebar.write("## Upload and download :gear:")
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    col1, col2 = st.columns(2)
    my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    img_file_buffer = st.camera_input("Take a photo of barcodes")

    # Photo taker
    if img_file_buffer is not None:
        # To read image file buffer as bytes:
        bytes_photo = img_file_buffer.getvalue()
        # Check the type of bytes_data:
        # Should output: <class 'bytes'>
        print(type(bytes_photo))
        generate_output(image=bytes_photo)

    # File downloader
    if my_upload:
        print(type(my_upload))
        if my_upload.size > MAX_FILE_SIZE:
            st.error("The uploaded file is too large. Please upload an image smaller than 10MB.")
        else:
            generate_output(image=Image.open(my_upload))
