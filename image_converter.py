import os
from PIL import Image

def convert_to_webp(input_file, output_file):
    image = Image.open(input_file)
    image.save(output_file, format='webp')

input_directory = "/home/muhammadsameer/Desktop/Office/Files/ImagesWebp/input_directory"
output_directory = "/home/muhammadsameer/Desktop/Office/Files/ImagesWebp/output_directory"

for filename in os.listdir(input_directory):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        input_file = os.path.join(input_directory, filename)
        output_file = os.path.join(output_directory, os.path.splitext(filename)[0] + ".webp")
        convert_to_webp(input_file, output_file)
