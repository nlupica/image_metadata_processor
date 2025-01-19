import os
import json
import logging
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ExifTags, ImageColor

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration file
CONFIG_FILE = "config.json"

# Ensure the config file exists
def ensure_config():
    if not os.path.exists(CONFIG_FILE):
        logging.error(f"Configuration file {CONFIG_FILE} is missing.")
        raise FileNotFoundError(f"Configuration file {CONFIG_FILE} is required but not found.")

# Load configuration
def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# Extract metadata from an image
def extract_metadata(image_path, fields):
    try:
        img = Image.open(image_path)
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in ExifTags.TAGS
        }
        return {field: exif.get(field, "N/A") for field in fields}
    except Exception as e:
        logging.warning(f"Failed to extract metadata from {image_path}: {e}")
        return {}

# Extract all metadata fields and save to a text file
def list_metadata_fields(image_path, output_file):
    try:
        img = Image.open(image_path)
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in ExifTags.TAGS
        }
        with open(output_file, "w") as f:
            for field in exif.keys():
                f.write(f"{field}\n")
        logging.info(f"Metadata fields saved to {output_file}")
    except Exception as e:
        logging.error(f"Failed to list metadata fields from {image_path}: {e}")

# Draw metadata on image
def annotate_image(image_path, output_path, metadata, config):
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img, "RGBA")

        # Load font
        font_path = config["text"].get("font", "arial.ttf")
        font_size = config["text"].get("size", 20)
        line_spacing = config["text"].get("line_spacing", 5)
        bold_color = config["text"].get("bold_color", "red")
        font = ImageFont.truetype(font_path, font_size)

        # Optionally add image name to metadata
        if config.get("add_image_name", False):
            image_name = os.path.basename(image_path)
            metadata = {"Image Name": image_name, **metadata}

        # Prepare metadata text
        lines = [f"{k}: {v}" for k, v in metadata.items()]
        line_height = font.getbbox("A")[3] - font.getbbox("A")[1]  # Height of a single line
        total_line_height = line_height + line_spacing
        text_width = max(font.getbbox(line)[2] - font.getbbox(line)[0] for line in lines)  # Max width of lines
        text_height = len(lines) * total_line_height

        # Calculate positions
        padding = config["text_box"].get("padding", 10)
        margin = config["text_box"].get("margin", 20)
        x, y = margin, margin
        box_coords = [x - padding, y - padding, x + text_width + padding, y + text_height + padding]

        # Draw text box
        box_color = config["text_box"].get("color", "black")
        opacity = config["text_box"].get("opacity", 128)
        border_color = config["text_box"].get("border_color", "gray")
        rgba_color = ImageColor.getrgb(box_color) + (opacity,)
        draw.rectangle(box_coords, fill=rgba_color, outline=border_color)

        # Draw text line by line
        for i, line in enumerate(lines):
            key, value = line.split(": ", 1)
            draw.text((x, y + i * total_line_height), f"{key}: ", fill=bold_color, font=font)
            text_offset = font.getbbox(f"{key}: ")[2]
            draw.text((x + text_offset, y + i * total_line_height), value, fill=config["text"].get("color", "white"), font=font)

        # Save output
        img.save(output_path)
        logging.info(f"Processed image saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to annotate image {image_path}: {e}")

# Main processing function
def process_images():
    config = load_config()
    raw_dir = config["raw_dir"]
    processed_dir = config["processed_dir"]
    suffix = config["output"].get("suffix", "_w_meta")

    for root, _, files in os.walk(raw_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(root, file)
                base, ext = os.path.splitext(file)
                output_file = f"{base}{suffix}{ext}"
                output_path = os.path.join(processed_dir, output_file)

                metadata = extract_metadata(input_path, config["metadata_fields"])
                annotate_image(input_path, output_path, metadata, config)

# Command-line entry point
def main():
    ensure_config()

    # Example of listing metadata fields for the first image in Raw Images
    sample_image = None
    config = load_config()
    raw_dir = config["raw_dir"]

    for root, _, files in os.walk(raw_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                sample_image = os.path.join(root, file)
                break
        if sample_image:
            break

    if sample_image:
        list_metadata_fields(sample_image, "metadata_fields.txt")
    else:
        logging.warning("No images found in Raw Images to list metadata fields.")

    process_images()

if __name__ == "__main__":
    main()
