from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import shutil

load_dotenv()

#API_KEY = os.getenv("API_KEY")
API_KEY = "AIzaSyALnqAOVedZHSnC2StN6D2xDR1cVGvaIUA" #I know it should be hidden but I couldnt get it to work on NCC with the api key hidden in .env :(


client = genai.Client(api_key=API_KEY)

output_dir = "ARMAN/generated_animal_images"
os.makedirs(output_dir, exist_ok=True)

MD_FILE = "ARMAN/challenge1.md"

animals = []

with open(MD_FILE, "r") as f:
    lines = [line.strip() for line in f]

mode = None 

for line in lines:

    if "Sort the animals" in line:
        continue

    elif line.startswith("## Animals"):
        mode = "animals"
        continue
    elif line.startswith("## Correct Order"):
        continue

    if mode == "animals":
        if line.startswith("- **") and line.endswith("**"):
            animal = line[4:-2]
            animals.insert(0, animal)

for filename in os.listdir(output_dir):
    file_path = os.path.join(output_dir, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)  # delete file
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  # delete folder inside it
    except Exception as e:
        print(f"Failed to delete {file_path}: {e}")

count = 1
for animal in animals:

    prompt = f"High-quality realistic photo of a {animal}"
    print(f"Generating image for: {animal}")

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT","IMAGE"]
        )
    )

    for part in response.parts:
        if part.inline_data is not None:
            # part.as_image() returns a PIL.Image
            img = part.as_image()
            file_path = os.path.join(output_dir, f"{count}.png")
            img.save(file_path)
            print(f"Saved image to {file_path}")
    
    count += 1
