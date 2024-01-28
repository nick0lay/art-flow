import os
from PIL import Image


def convert_to_pixels(size, unit, ppi=300):
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


def resize(src: str, dist: str, size: tuple[int, int], unit, ppi) -> None:
    """
    Resize images to predefined sizes. List all images in input folder, resize
    and put them into a corresponding structure in the output folder.
    """
    size_pixel = convert_to_pixels(size, unit, ppi)
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

                img_resized.save(output_path, dpi=(ppi, ppi))

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