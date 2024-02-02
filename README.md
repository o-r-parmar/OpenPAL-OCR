# OpenPAL-OCR
The script captures screenshots at specified coordinates within the OpenPAL software, converting these images into .csv file outputs.

# Image Processing and OCR Script

This Python script automates the process of cropping images, applying threshold adjustments, performing optical character recognition (OCR), and converting the extracted text into a CSV file format.

## Requirements

To run this script, you need Python 3 and the following packages:

- `Pillow` for image processing.
- `pytesseract` for OCR capabilities.
- `glob` and `os` for file and directory operations.
- `csv` and `re` for CSV operations and regular expressions, respectively.

## Installation

First, ensure you have Python 3 installed on your system. Then, install the required Python packages using pip:

```bash
pip install Pillow pytesseract
```

**Note**: `pytesseract` requires the Tesseract-OCR engine to be installed on your system. Visit the [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract) for installation instructions specific to your operating system.

## Usage

1. Paste the required images in the Images folder
2. Modify the `directory`, `save_directory`, `txt_directory`, and `csv_directory` variables in the script to point to your desired input and output directories.
3. Run the script using Python:

```bash
python script.py
```
