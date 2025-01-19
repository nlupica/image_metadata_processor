# Image Metadata Processor

## Liability Statement

**This software is provided on an "as is" basis, without any warranties of any kind, either express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement. In no event shall the authors or contributors be held liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services, loss of use, data, or profits) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.**

## Project Overview

The Image Metadata Processor is a Python-based tool that extracts metadata from images, overlays the metadata on the images, and saves the processed images to a specified directory. This tool is customizable through a configuration file and supports efficient metadata field selection and visualization.

## Prerequisites

- Python 3.7 or higher
- Pip (Python package installer)
- Images from the same camera source or with the same metadata fields.

## Setup Steps

### 1. Clone the GitHub Repository

```bash
git clone <repository_url>
cd <repository_name>
```

### 2. Install Dependencies

Make sure to install the required Python libraries from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Ensure the Input and Output Directories Exist

Create the following directories if they do not already exist:

- `Raw Images/`: Place your input images here.
- `Processed Images/`: The output directory for processed images.

### 4. Configure the Application

Modify the `config.json` file to specify your preferences. See the **Configuration Details** section below for detailed explanations. NOTE: By default, the configuration settings are already tuned for good visibility of metadata. However, depending on your image's metadata, specific keys may need to be updated in the metadata_fields list within the config file.

### 5. Run the Application

To process the images:

```bash
python metadata_processor.py
```

## Configuration Details

The application uses a `config.json` file to define settings. Below are the available configuration options:

### General Settings

- `raw_dir`: Directory where input images are stored. (NOTE: this should probably remain unchanged)
- `processed_dir`: Directory where processed images will be saved. (NOTE: this should probably remain unchanged)

### Metadata Fields

- `metadata_fields`: List of EXIF metadata fields to extract and overlay on images. Examples include:
  - `DateTime`
  - `Make`
  - `Model`

NOTE: These fields are dependant on your own image's metadata. With the assumption that all images are captured by the same camera, the metadata_fields.txt file will have all metadata keys available. If you have multiple images with different capture methods, these fields may have varying names, which may cause the code to break.

### Text Box Customization

- `text_box.color`: Background color of the metadata text box (e.g., `"black"`, `"gray"`).
- `text_box.opacity`: Opacity of the background box (0-255).
- `text_box.padding`: Padding between the text and the edges of the box.
- `text_box.margin`: Margin from the top-left corner of the image.
- `text_box.border_color`: Border color of the text box.

### Text Customization

- `text.font`: Font (e.g., `"arial.ttf"`).
- `text.size`: Font size.
- `text.color`: Font color for the metadata values.
- `text.bold_color`: Font color for the metadata keys.
- `text.line_spacing`: Space between lines of text.

### Output Customization

- `output.suffix`: Suffix appended to processed image filenames (e.g., `"_w_meta"`).

### Optional Features

- `add_image_name`: If `true`, the image file name is included as the first metadata field.

## Exploring Metadata Fields

To explore all available metadata fields for an image:

1. Place an image in the `Raw Images/` directory.
2. Run the following command to generate a text file listing the metadata fields:
   ```bash
   python metadata_processor.py
   ```
3. Check the `metadata_fields.txt` file in the root directory.
4. Identify fields of interest and add them to the `metadata_fields` section in `config.json` for overlay inclusion.

### Example Metadata Fields

Example output of `metadata_fields.txt`:

```
DateTime
Make
Model
```

You can add any of these fields to the `metadata_fields` array in `config.json` to include them in the image annotations.

## Example Workflow

1. Place your images in the `Raw Images/` folder.
2. Update the `metadata_fields` in `config.json` with fields like `Make`, `Model`, and `DateTime`.
3. Run the script.
4. Find processed images with overlaid metadata in the `Processed Images/` folder.
