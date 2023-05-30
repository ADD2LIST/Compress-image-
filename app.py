import streamlit as st
import os
from PIL import Image

# Get the Image Size
def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

# To compress the given image
def compress_given_img(image_name, new_size_ratio=0.9, quality=90, image_width=None, height_width=None, to_jpg=True):
    # loading the uploaded image to memory
    img = Image.open(image_name)
    # printing the original image shape
    st.write("[*] The size of image:", img.size)
    # getting the original image size in bytes
    image_size = os.path.getsize(image_name)
    # printing the size before compression/resizing
    st.write("[*] Size before compression:", get_size_format(image_size))
    if new_size_ratio < 1.0:
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        # print new image shape
        st.write("New Image shape:", img.size)
    elif image_width and height_width:
        # if image_width and height_width are set, resize with them instead
        img = img.resize((image_width, height_width), Image.ANTIALIAS)
        # print new image shape
        st.write("New Image shape:", img.size)
    # split the filename and extension
    filename, ext = os.path.splitext(image_name)
    # make new filename appending _compressed to the original file name
    if to_jpg:
        # change the extension to JPEG
        new_filename = f"{filename}_compressed.jpg"
    else:
        # retain the same extension of the original image
        new_filename = f"{filename}_compressed{ext}"
    try:
        # save the image with the corresponding quality and optimize set to True
        img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        # convert the image to RGB mode first
        img = img.convert("RGB")
        # save the image with the corresponding quality and optimize set to True
        img.save(new_filename, quality=quality, optimize=True)
    st.write("New file saved:", new_filename)
    # get the new image size in bytes
    new_image_size = os.path.getsize(new_filename)
    # print the new size in a good format
    st.write("Size after compression:", get_size_format(new_image_size))
    # calculate the saving bytes
    saving_diff = new_image_size - image_size
    # print the saving percentage
    st.write(f"Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")

def main():
    st.title("Image Compression")
    image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if image_file is not None:
        st.write("Image uploaded successfully!")
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        options = st.beta_columns(2)
        new_size_ratio = options[0].slider("Resize Ratio", 0.1, 1.0, 0.9, 0.05)
        quality = options[1].slider("Quality", 0, 95, 90)
        
        resize_option = st.radio("Resize Options", ["Keep Aspect Ratio", "Custom Size"])
        if resize_option == "Custom Size":
            width = st.number_input("Width", min_value=1, value=image.size[0])
            height = st.number_input("Height", min_value=1, value=image.size[1])
        else:
            width = None
            height = None

        to_jpg = st.checkbox("Convert to JPEG")

        if st.button("Compress"):
            compress_given_img(image_file, new_size_ratio, quality, width, height, to_jpg)

if __name__ == "__main__":
    main()
