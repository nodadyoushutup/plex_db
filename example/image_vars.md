The PIL.Image.save() method accepts various parameters depending on the image format. Here are some common parameters available for different formats when saving images:

Common Parameters (for most formats):
format: Specifies the file format (e.g., 'JPEG', 'PNG').
quality: For JPEG, this controls the compression level. Values range from 1 (worst) to 95 (best), with a default of 75.
optimize: A Boolean flag (True/False). If True, the encoder will make an extra pass over the image to select optimal settings for saving (available for formats like JPEG).
progressive: For JPEG, enables saving the image in progressive format, which is useful for web images as it displays a lower-quality preview before fully downloading the image.
dpi: A tuple (x, y) that sets the DPI (dots per inch) for the image. This is useful for print images.
icc_profile: Embeds a color profile (for JPEG, PNG, etc.).
exif: Allows adding EXIF metadata to JPEG images. You can pass binary EXIF data here.
Format-Specific Parameters:
1. JPEG
quality: Compression level (1-95).
optimize: Boolean. If True, optimizes the saved image size.
progressive: Boolean. If True, saves as a progressive JPEG.
subsampling: Sets subsampling for JPEG compression (default: 0). Can be 0, 1, or 2. Lower subsampling means better quality but larger file size.
dpi: Tuple for setting DPI (e.g., (300, 300) for print).
exif: Adds EXIF metadata to the saved JPEG.
icc_profile: Embeds an ICC color profile.
2. PNG
compress_level: Compression level for PNG images (0-9). 0 means no compression, 9 is maximum compression.
dpi: Similar to JPEG, sets DPI for the PNG image.
icc_profile: Embeds a color profile.
transparency: Passes transparency data for the image (usually a palette index).
tRNS: A list of transparency data for grayscale or true-color images.
pnginfo: Allows passing metadata to the PNG file (like text or time information).
3. GIF
save_all: Boolean flag. If True, saves all frames in an image (useful for animated GIFs).
append_images: List of additional frames to append to the GIF.
duration: Specifies the duration between frames (in milliseconds) for animated GIFs.
loop: Number of times the GIF animation will loop. 0 means infinite loop.
transparency: Adds transparency by specifying a color index for transparency.
disposal: Specifies how the GIF frame should be disposed after it is displayed.
4. TIFF
compression: Sets the compression type for TIFF images. Options include None, tiff_lzw, tiff_jpeg, tiff_adobe_deflate, etc.
dpi: Similar to JPEG and PNG.
icc_profile: Embeds a color profile.
resolution: Sets resolution for the TIFF image.
5. BMP
dpi: Similar to JPEG, PNG, and TIFF.