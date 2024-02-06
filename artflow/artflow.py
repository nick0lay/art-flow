import click
import image as image_actions

@click.group()
def cli():
    """Main command group for the application."""
    pass


@cli.group()
def image():
    """Commands related to image operations."""
    pass


@image.command()
@click.option("--src", default="./input", help="Folder with images to resize.")
@click.option("--dist", default="./output", help="Folder to save resized images.")
@click.option(
    "--size",
    nargs=2,
    type=int,
    default=(30, 40),
    help="New size for images as width height.",
)
@click.option(
    "--unit",
    type=click.Choice(["cm", "in"], case_sensitive=False),
    default="cm",
    help="Unit of the size (cm or in).",
)
@click.option("--ppi", type=int, default=300, help="Pixels Per Inch for conversion.")
def resize(src, dist, size, unit, ppi):
    """
    Resize images to predefined sizes. List all images in input folder, resize
    and put them into a corresponding structure in the output folder.
    """
    click.echo("Resizing images...")
    image_actions.resize(src, dist, size, unit, ppi)

# @image.command()
# @click.argument('image_path')
# @click.option('--ratios', default="2x3,3x4,4x5,iso,11x14", help="Aspect ratios to use for cropping.")
# def crop(image_path, ratios):
#     """Crop the image at the center using the provided list of aspect ratios."""
#     selected_ratios = ratios.split(',')
#     image_actions.crop(image_path, selected_ratios)

@image.command()
@click.option("--src", default="./input", help="Folder with images to resize.")
@click.option("--dist", default="./output", help="Folder to save resized images.")
@click.option('--ratios', default="2x3,3x4,4x5,iso,11x14", help="Aspect ratios to use for cropping.")
def crop(src, dist, ratios):
    """Crop the image at the center using the provided list of aspect ratios."""
    selected_ratios = ratios.split(',')
    click.echo("Cropping images...")
    image_actions.crop_all(src, dist, selected_ratios)

if __name__ == '__main__':
    cli()