import glob
import os
import cv2

import face_recognition
from PIL import Image

# Load the jpg file into a numpy array
count = 0
image_path = "CroppedImages"

os.makedirs(image_path, exist_ok=True)
for image_file in glob.glob("Photos/*.jpg"):
    image = face_recognition.load_image_file(image_file)

    face_locations = face_recognition.face_locations(image)

    number_of_faces = len(face_locations)
    print(f"Found {number_of_faces} face(s) in the photograph {image_file}")

    pil_image = Image.open(image_file)
    for face_location in face_locations:
        top, right, bottom, left = face_location
        cropped_image = pil_image.crop((left, top, right, bottom))
        cropped_image = cropped_image.resize(pil_image.size, Image.Resampling.LANCZOS)
        cropped_image.save(f"{image_path}/image{count}.jpg")
        print(cropped_image.size)

        count += 1

