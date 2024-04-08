import streamlit as st
from fpdf import FPDF
from PIL import Image
import os

def convert_to_png(image_folder):
    # Get all image files in the specified folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Loop through each image file and convert it to PNG format
    for image_file in image_files:
        try:
            # Open the image file using PIL
            image_path = os.path.join(image_folder, image_file)
            img = Image.open(image_path)

            # Convert the image to PNG format
            if img.format != "PNG":
                img = img.convert("RGB")
                img.save(image_path, format="PNG")
        except Exception as e:
            st.error(f"Error converting image '{image_file}' to PNG format: {e}")

def images_to_pdf(image_folder, output_pdf):
    # Create a PDF object
    pdf = FPDF()

    # Get all image files in the specified folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

    # Loop through each image file and add it to the PDF
    for image_file in image_files:
        try:
            # Open the image file using PIL
            image_path = os.path.join(image_folder, image_file)
            img = Image.open(image_path).convert("RGB")  # Convert image to RGB format

            # Add a page to the PDF
            pdf.add_page()

            # Calculate image dimensions to fit the page
            width, height = img.size
            if width > height:
                pdf.image(image_path, 0, 0, w=210)
            else:
                pdf.image(image_path, 0, 0, h=297)
        except Exception as e:
            st.error(f"Error processing image '{image_file}': {e}")

    # Save the PDF
    pdf.output(output_pdf)
    st.success(f"PDF file '{output_pdf}' created successfully.")

def main():
    st.title("Image to PDF Converter")

    # Upload multiple image files
    uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        # Create a folder to store the uploaded images
        os.makedirs("uploaded_images", exist_ok=True)

        # Save uploaded images to the folder and convert them to PNG
        for i, uploaded_file in enumerate(uploaded_files):
            with open(os.path.join("uploaded_images", f"image_{i}.png"), "wb") as f:
                f.write(uploaded_file.getbuffer())

        # Convert all images to PNG format
        convert_to_png("uploaded_images")

        # Get desired PDF file name from user
        desired_pdf_name = st.text_input("Enter desired name for PDF file (without extension):")

        # Convert images to PDF with the desired name
        if desired_pdf_name:
            pdf_filename = f"{desired_pdf_name}.pdf"
            images_to_pdf("uploaded_images", pdf_filename)

            # Add a download button for the generated PDF
            st.download_button(label="Download PDF", data=open(pdf_filename, "rb").read(), file_name=pdf_filename)

if __name__ == "__main__":
    main()
