import os
import glob
from PIL import Image, ImageEnhance
import pytesseract
import csv
import re


def crop_image(directory=None, save_directory=None, pattern=None):
    if not os.path.exists(directory):
        # Create the directory since it does not exist
        os.makedirs(directory)
    
    if not os.path.exists(save_directory):
        # Create the directory since it does not exist
        os.makedirs(save_directory)

    # Loop through all matching files
    for file_path in glob.glob(os.path.join(directory, pattern + "*.png")):
        
        # Extract file name from the path
        file_name = os.path.basename(file_path)

        # Open the image
        image = Image.open(file_path)

        # Scale the image by 5 times
        scaled_image = image.resize((image.width * 15, image.height * 15))

        # Define the coordinates of the crop (adjust these values for the scaled image)
        crop_box = (240 * 15, 584 * 15, 1092 * 15, 620 * 15)

        # Crop the image
        cropped_image = scaled_image.crop(crop_box)

        # Remove the pattern from the file name for the cropped version
        cropped_file_name = 'image_' + file_name.replace(pattern, '').strip()

        # Save the cropped image
        cropped_image.save(os.path.join(save_directory, cropped_file_name))
        print(f"Cropped Image Saved: {cropped_file_name}")

def crop_time(directory=None, save_directory=None, pattern=None):
    # Loop through all matching files
    for file_path in glob.glob(os.path.join(directory, pattern + "*.png")):
        # Extract file name from the path
        file_name = os.path.basename(file_path)

        # Open the image
        image = Image.open(file_path)

        # Scale the image by 5 times
        scaled_image = image.resize((image.width*15, image.height*15))

        # Define the coordinates of the crop (adjust these values for the scaled image)
        crop_box = (1714*15, 1011*15, 1816*15, 1048*15)

        # Crop the image
        cropped_image = scaled_image.crop(crop_box)

        # Remove the pattern from the file name for the cropped version
        cropped_file_name = 'time_' + file_name.replace(pattern, '').strip()

        # Save the cropped image
        cropped_image.save(os.path.join(save_directory, cropped_file_name))
        print(f"Cropped Image Saved: {cropped_file_name}")

def threshold(directory=None):
    for file_path in glob.glob(os.path.join(directory, "*.png")):
        # Open the image
        image = Image.open(file_path)

        # Convert the image to grayscale
        gray_image = image.convert('L')

        # Enhance the image contrast
        enhancer = ImageEnhance.Contrast(gray_image)
        enhanced_image = enhancer.enhance(2)  # The enhancement factor can be tuned

        # Apply thresholding to get a clearer, binary image
        threshold_value = 110  # Threshold value can be tuned for different images
        bw_image = enhanced_image.point(lambda x: 255 if x > threshold_value else 0, '1')

        # Overwrite the original image with the thresholded image
        bw_image.save(file_path)

def ocr(directory=None):
    if directory is None:
        print("Directory is not specified.")
        return
    
    all_text = ""
    times_dict = {}
    custom_config = r'--oem 3 --psm 9 --user-patterns text_pattern.txt -c tessedit_char_whitelist=0123456789e+.,-:'
    
    text_file_path = os.path.join(directory, 'combined_ocr_text.txt')

    if not os.path.exists(directory):
        # Create the directory since it does not exist
        os.makedirs(directory)
    
    with open(text_file_path, 'w') as file:
        file.write("")

    # Adjusting regex to match filenames with parentheses around the number
    for time_path in glob.glob(os.path.join(directory, "time_(*).png")):
        match = re.search(r'time_\((\d+)\).png', time_path)
        if match:
            number = match.group(1)
            time_text = pytesseract.image_to_string(Image.open(time_path), config=custom_config).strip()
            times_dict[number] = time_text

    for image_path in glob.glob(os.path.join(directory, "image_(*).png")):
        match = re.search(r'image_\((\d+)\).png', image_path)
        if match:
            number = match.group(1)
            if number in times_dict:
                image_text = pytesseract.image_to_string(Image.open(image_path), config=custom_config).strip()
                time_text = times_dict.get(number, "")
                combined_text = f"{time_text} | {image_text}\n"
                all_text += combined_text
    
    with open(text_file_path, 'a') as file:
        file.write(all_text)

def txt2csv(directory=None, save_directory=None):
    with open(directory, 'r') as infile, open(save_directory, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        # Adjust the header to include the 'Time' column
        csv_writer.writerow(['Time', 'x', 'y', 'z', 'Rx', 'Ry', 'Rz'])

        for line in infile:
            # Split the line at '|' to separate time from data
            time_part, data_part = line.strip().split(' | ')
            # Split the time using ':', which separates hours and minutes
            hours, minutes = time_part.split(':')
            # Format the time as needed; here, keeping it as "hours:minutes"
            time_formatted = f"{hours}:{minutes}"
            # Split the data part by commas and convert each piece to a float
            row = [float(value) for value in data_part.split(',')]
            # Prepend the formatted time to the row
            csv_writer.writerow([time_formatted] + row)

    print(f"File converted to CSV and saved as '{save_directory}'")

directory = './Images/'
save_directory ='./Images/cropped_images/'
txt_directory = './Images/cropped_images/combined_ocr_text.txt'
csv_directory = 'combined_csv_data.csv'


crop_image(directory=directory, save_directory=save_directory, pattern='Screenshot')
crop_time(directory=directory, save_directory=save_directory, pattern='Screenshot')
threshold(directory=save_directory)
ocr(directory=save_directory)
txt2csv(directory=txt_directory, save_directory=csv_directory)