import os
from utils.image_utils import anonymize_image
from dotenv import load_dotenv

load_dotenv()

def main():
    
    input_dir = "input_images"
    output_dir = "output_images"
    instructions_file = "instructions.txt"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(instructions_file, 'r') as f:
            instructions = f.read()
    except FileNotFoundError:
        print(f"Error: {instructions_file} not found.")
        return

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            print(f"Processing {input_path}...")
            anonymize_image(input_path, output_path, instructions)

if __name__ == "__main__":
    main()
