import os
import random
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import random
from noise import pnoise2
from scipy import ndimage
import os

def create_directory(dir_name):
    """
    Creates a new directory with the given name at the specified path.
    If the directory already exists, appends an integer to the end of the name to make it unique.
    """
    # Define the path to the directory
    path = os.path.dirname(os.path.realpath(__file__))
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


def generate_circles(num_images, image_size, num_circles, min_radius, max_radius, train_perc, test_perc):
    
    # Create directories for train, test, and validation sets
    base_dir_name = f"data/SAIL/motion_planning_datasets/C_setC{num_images}_size{image_size}_circC{num_circles}_minRad{min_radius}_maxRad{max_radius}"
    train_dir_name = f"{base_dir_name}/train"
    test_dir_name = f"{base_dir_name}/test"
    val_dir_name = f"{base_dir_name}/validation"

    # Create new directories for the images
    train_dir_path = create_directory(base_dir_name)
    train_dir_path = create_directory(train_dir_name)
    test_dir_path = create_directory(test_dir_name)
    val_dir_path = create_directory(val_dir_name)

    # Generate random images with circles and save them to their respective directories
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

       # Determine which directory to save the image to
        rand_num = random.random()
        if rand_num < train_perc:
            dir_path = train_dir_path
        elif rand_num < train_perc + test_perc:
            dir_path = test_dir_path
        else:
            dir_path = val_dir_path

        # Save the image to a file
        filename = f'image_{i}.png'
        img.save(os.path.join(dir_path, filename))

    for dir in [train_dir_name, test_dir_name, val_dir_name]:
        for filename in os.listdir(dir):
            if filename.endswith('.png'):
                # open the image file
                filepath = os.path.join(dir, filename)
                with Image.open(filepath) as img:
                    # resize the image to 200 by 200
                    img = img.resize((200, 200))
                    # save the resized image
                    img = img.convert('1')
                    img.save(filepath)

    print(f"{num_images} images generated and saved successfully.")

def generate_triangles(num_images, image_size, num_triangles, min_size, max_size, train_perc, test_perc):
    
    # Define the name of the directory to be created
    base_dir_name = f"data/SAIL/motion_planning_datasets/T_setC{num_images}_size{image_size}_triC{num_triangles}_minSize{min_size}_maxSize{max_size}"
    train_dir_name = f"{base_dir_name}/train"
    test_dir_name = f"{base_dir_name}/test"
    val_dir_name = f"{base_dir_name}/validation"

    # Create new directories for the images
    train_dir_path = create_directory(base_dir_name)
    train_dir_path = create_directory(train_dir_name)
    test_dir_path = create_directory(test_dir_name)
    val_dir_path = create_directory(val_dir_name)

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

        # Determine which directory to save the image to
        rand_num = random.random()
        if rand_num < train_perc:
            dir_path = train_dir_path
        elif rand_num < train_perc + test_perc:
            dir_path = test_dir_path
        else:
            dir_path = val_dir_path

        # Save the image to a file
        filename = f'image_{i}.png'
        img.save(os.path.join(dir_path, filename))

    for dir in [train_dir_name, test_dir_name, val_dir_name]:
        for filename in os.listdir(dir):
            if filename.endswith('.png'):
                # open the image file
                filepath = os.path.join(dir, filename)
                with Image.open(filepath) as img:
                    # resize the image to 200 by 200
                    img = img.resize((200, 200))
                    img = img.convert('1')
                    # save the resized image
                    img.save(filepath)



def generate_perlinnoise(num_images, image_size, freq2, oct_bound_l, oct_bound_u, threshold2, train_perc, test_perc):

    base_dir_name = f"data/SAIL/motion_planning_datasets/PN_setC{num_images}_size{image_size}_freq{freq2}_octl{oct_bound_l}_octu{oct_bound_u}_V"

    train_dir_name = f"{base_dir_name}/train"
    test_dir_name = f"{base_dir_name}/test"
    val_dir_name = f"{base_dir_name}/validation"

    # Create new directories for the images
    train_dir_path = create_directory(base_dir_name)
    train_dir_path = create_directory(train_dir_name)
    test_dir_path = create_directory(test_dir_name)
    val_dir_path = create_directory(val_dir_name)
    
    # iterate over each image to generate
    for i in range(num_images):
 
        width=image_size
        height=image_size
        # create a new image with a white background
        img = Image.new('RGB', (width, height), color='white')
    
        # create a pixel access object
        pixels = img.load()
    
        
        # generate a random frequency between a min and max value
        freq_min = 4
        freq_max = freq2
        freq = random.uniform(freq_min, freq_max)

        # generate a random number of octaves between a min and max value
     
        octaves = random.randint(oct_bound_l, oct_bound_u)
    
        # generate a 2D grid of noise values
        noise_grid = [[pnoise2(x / freq, y / freq, octaves) for y in range(height)] for x in range(width)]
    
        # set the threshold value for creating shapes
        threshold = threshold2 * random.randrange(1100,3700,1)/1000
    
        # create a mask image with black and white pixels
        mask = Image.new('1', (width, height), color=1)
        mask_pixels = mask.load()
    
        # iterate over each pixel in the noise grid
        for x in range(width):
            for y in range(height):
                # if the noise value is above the threshold, set the pixel in the mask to black
                if noise_grid[x][y] > threshold:
                    mask_pixels[x, y] = 0
                # otherwise, set the pixel in the original image to white
                else:
                    pixels[x, y] = (255, 255, 255)
    
        # use the flood fill algorithm to fill any isolated white spaces
        mask_array = np.array(mask)
        structure = np.ones((3,3))
        label_array, num_labels = ndimage.label(mask_array, structure=structure)
        mask_array[label_array == 0] = 0
        mask = Image.fromarray(mask_array.astype(np.uint8))
    
        # iterate over each pixel in the mask and set the corresponding pixel in the original image to black
        for x in range(width):
            for y in range(height):
                if mask_pixels[x, y] == 0:
                    pixels[x, y] = (0, 0, 0)


        # Determine which directory to save the image to
        rand_num = random.random()
        if rand_num < train_perc:
            dir_path = train_dir_path
        elif rand_num < train_perc + test_perc:
            dir_path = test_dir_path
        else:
            dir_path = val_dir_path

        # Save the image to a file
        filename = f'image_{i}.png'
        # Load the image

# Generate a random angle between -45 and 45 degrees

        multiple = random.randint(0, 3) * 90

# Rotate the image by the generated multiple of 90 degrees
        img = img.rotate(multiple)

# Save the rotated image
        img.save(os.path.join(dir_path, filename))

    for dir in [train_dir_name, test_dir_name, val_dir_name]:
        for filename in os.listdir(dir):
            if filename.endswith('.png'):
                # open the image file
                filepath = os.path.join(dir, filename)
                with Image.open(filepath) as img:
                    # resize the image to 200 by 200
                    img = img.resize((200, 200))
                    img = img.convert('1')
                    # save the resized image
                    img.save(filepath)


if __name__ == '__main__':
    #generate_circles(num_images=1000, image_size=256, num_circles=15, min_radius=15, max_radius=50, train_perc=0.8, test_perc=0.1)
    #generate_triangles(num_images=50, image_size=256, num_triangles=15, min_size=40, max_size=100, train_perc=0.8, test_perc=0.1)
    generate_perlinnoise(num_images=51, image_size=200, freq2=32, oct_bound_l=1, oct_bound_u=6, threshold2=0.05, train_perc=0.8, test_perc=0.1)

