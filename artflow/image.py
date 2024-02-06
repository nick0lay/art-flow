import os
from PIL import Image

DPI = 300
CM_TO_INCH = 2.54

# Define the aspect ratios and their max sizes (width x height in centimeters)
ASPECT_RATIOS = {
    '2x3': (50, 75),
    '3x4': (45, 60),
    '4x5': (40, 50),
    'iso': (50, 70),  # Assuming 'iso' refers to a specific ratio here; adjust as needed
    '11x14': (11*CM_TO_INCH, 14*CM_TO_INCH)
}

def convert_to_pixels(size, unit='cm', ppi=300):
    """
    Convert size from cm or inches to pixels based on PPI (Pixels Per Inch).

    :param size: Tuple (width, height) in cm or inches.
    :param unit: 'cm' for centimeters or 'in' for inches.
    :param ppi: Pixels Per Inch, default is 300.
    :return: Tuple (width, height) in pixels.
    """
    if unit == 'cm':
        # 1 inch = 2.54 cm
        return int(size[0] / 2.54 * ppi), int(size[1] / 2.54 * ppi)
    elif unit == 'in':
        return int(size[0] * ppi), int(size[1] * ppi)
    else:
        raise ValueError("Invalid unit. Only 'cm' and 'in' are accepted.")

def calculate_crop_dimensions(original_size, target_size):
    orig_width, orig_height = original_size
    target_width, target_height = target_size

    # Calculate the scaling factor
    scale = min(orig_width / target_width, orig_height / target_height)

    # Calculate the new width and height based on the aspect ratio
    new_width = scale * target_width
    new_height = scale * target_height

    # Calculate the position to start the crop from (to center the crop)
    left = (orig_width - new_width) / 2
    top = (orig_height - new_height) / 2

    return (int(left), int(top), int(left + new_width), int(top + new_height))

def resize(src: str, dist: str, size: tuple[int, int], unit, dpi=DPI) -> None:
    """
    Resize images to predefined sizes. List all images in input folder, resize
    and put them into a corresponding structure in the output folder.
    """
    size_pixel = convert_to_pixels(size, unit, dpi)
    for subdir, dirs, files in os.walk(src):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                img_path = os.path.join(subdir, file)
                img = Image.open(img_path)
                print(size_pixel)
                img_resized = img.resize(size_pixel)

                relative_path = os.path.relpath(subdir, src)
                output_subdir = os.path.join(dist, relative_path)

                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)

                file_name, file_ext = os.path.splitext(file)
                output_file_name = f"{file_name}_{size[0]}x{size[1]}{file_ext}"
                output_path = os.path.join(output_subdir, output_file_name)

                img_resized.save(output_path, dpi=(dpi, dpi))

def create_source_image(input_path: str, filename: str):
    """
    Create a source image at 300 DPI and place it in a tmp folder inside the input folder.

    :param input_path: Path to the original image.
    :param output_folder: Folder where the tmp folder will be created.
    :param filename: Name of the generated source image.
    """
    tmp_folder = os.path.join(input_path, "tmp")
    os.makedirs(tmp_folder, exist_ok=True)

    img = Image.open(input_path)
    # Assuming the image is in RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')

    dpi = (300, 300)
    image_path = os.path.join(tmp_folder, filename)
    img.save(image_path, dpi=dpi)
    return image_path

def crop(image_path: str, selected_ratios: list[str], dpi=DPI) -> None:
    with Image.open(image_path) as img:
        for ratio in selected_ratios:
            if ratio in ASPECT_RATIOS:
                size_cm = ASPECT_RATIOS[ratio]
                target_size = convert_to_pixels(size_cm)
                crop_dimensions = calculate_crop_dimensions(img.size, target_size)

                cropped_img = img.crop(crop_dimensions)

                # Save the cropped image
                file_name, file_ext = os.path.splitext(image_path)
                print(file_name, file_ext)
                output_filename = f"{file_name}_{ratio}.{file_ext}"

                cropped_img.save(output_filename, dpi=(dpi, dpi))
                print(f"Cropped {image_path} to {ratio} and saved as {output_filename}")
            else:
                print(f"Unsupported ratio: {ratio}")

def crop_all(src: str, dist: str, selected_ratios: list[str], dpi=DPI) -> None:
    for subdir, dirs, files in os.walk(src):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                img_path = os.path.join(subdir, file)
                crop(img_path, selected_ratios, dpi)
    print("All images cropped successfully.")