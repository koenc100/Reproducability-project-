import os
import random
from PIL import Image, ImageDraw, ImageOps
import numpy as np

def create_directory(dir_name):
    """
    Creates a new directory with the given name at the specified path.
    If the directory already exists, appends an integer to the end of the name to make it unique.
    """
    # Define the path to the directory
    path = r"C:\Users\koen6\OneDrive\Documenten\TU Delft\Masters\Year 2\Q3\Deep Learning\reproducability paper\repr_images"

    # Combine the path and directory name
    dir_path = os.path.join(path, dir_name)
    
    # Check if the directory already exists
    if os.path.exists(dir_path):
        i = 1
        while os.path.exists(dir_path + "_" + str(i)):
            i += 1
        dir_path = dir_path + "_" + str(i)
    
    # Create the new directory
    try:
        os.mkdir(dir_path)
        print(f"Directory '{dir_name}' created at path '{dir_path}'.")
    except OSError:
        print(f"Creation of directory '{dir_name}' failed at path '{dir_path}'.")
    
    return dir_path

def generate_circles(num_images, image_size, num_circles, min_radius, max_radius):
    
     # Define the name of the directory to be created
    dir_name = f"C_setC{num_images}_size{image_size}_circC{num_circles}_minRad{min_radius}_maxRad{max_radius}_V"

    # Create a new directory for the images
    dir_path = create_directory(dir_name)

    # Generate random images with circles
    for i in range(num_images):
        # Create a new image with white background
        img = Image.new('RGB', (image_size, image_size), color='white')
        draw = ImageDraw.Draw(img)

        # Draw random circles
        for j in range(num_circles):
            radius = random.randint(min_radius, max_radius)
            x = random.randint(radius, image_size - radius)
            y = random.randint(radius, image_size - radius)
            color = (0, 0, 0)  # black color
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

        # Save the image to a file
        filename = f'image_{i}.png'
        img.save(os.path.join(dir_path, filename))

def generate_triangles(num_images, image_size, num_triangles, min_size, max_size):

    # Create a new directory for the images
    dir_name  = f"T_setC{num_images}_size{image_size}_triC{num_triangles}_minSize{min_size}_maxSize{max_size}_V"
    
    # Create a new directory for the images
    dir_path = create_directory(dir_name)

    # Generate random images with triangles
    for i in range(num_images):
        # Create a new image with white background
        img = Image.new('RGB', (image_size, image_size), color='white')
        draw = ImageDraw.Draw(img)

        # Draw random triangles
        for j in range(num_triangles):
            size = random.randint(min_size, max_size)
            x1 = random.randint(0, image_size - size)
            y1 = random.randint(0, image_size - size)
            x2 = x1 + size
            y2 = y1 + size
            x3 = random.randint(x1, x2)
            y3 = random.randint(y1, y2)
            color = (0, 0, 0)  # black color
            draw.polygon([(x1, y1), (x2, y1), (x3, y3)], fill=color)

        # Save the image to a file
        filename = f'image_{i}.png'
        img.save(os.path.join(dir_path, filename))

if __name__ == '__main__':
    generate_circles(num_images=50, image_size=256, num_circles=5, min_radius=10, max_radius=50)
    generate_triangles(num_images=50, image_size=256, num_triangles=8, min_size=40, max_size=50)
