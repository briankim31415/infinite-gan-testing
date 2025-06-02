from PIL import Image
num = 7

# List your image file paths in the desired order
image_paths = [f"source_pics/{num}_samples.png", f"logs/plot_{num}_loss.png"]

# Open all images
images = [Image.open(p) for p in image_paths]

# Compute total width and max height
total_width = sum(img.width for img in images)
max_height = max(img.height for img in images)

# Create a new blank image
new_img = Image.new('RGB', (total_width, max_height), color=(255, 255, 255))

# Paste images side-by-side
x_offset = 0
for img in images:
    new_img.paste(img, (x_offset, 0))
    x_offset += img.width

# Save the final image
new_img.save(f"{num}_combined_plots.png")