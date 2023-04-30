'''
I have a folder "D:\dequi\Documents\mmimdb.tar\mmimdb\mmimdb\dataset" that contains. 
This folder contains images and json files. For each image, there is a json file. 
Write a python program that iterates over the images and json files, and copies to a folder 2000 images 
(with the corresponding json file) where the value of the attribute "genres" contains "Drama" and 2000 images 
(with the corresponding json file) where the value of the attribute "genres" contains "Horror". 
However, if both "Drama" and "Horror" are in this attribute, we should exclude them. 
'''

import os
import shutil
import json

drama_count = 0
horror_count = 0
target_dir = 'D:/dequi/Documents/mmimdb_horror_2000_drama_2000'

# Iterate over the files in the dataset folder
for filename in os.listdir('D:/dequi/Documents/mmimdb.tar/mmimdb/mmimdb/dataset'):
    if filename.endswith('.jpeg'):
        # Get the corresponding JSON filename
        json_filename = os.path.splitext(filename)[0] + '.json'
        json_path = os.path.join('D:/dequi/Documents/mmimdb.tar/mmimdb/mmimdb/dataset', json_filename)

        # Load the JSON file
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Check the genres attribute
        genres = data['genres']
        if 'Drama' in genres and 'Horror' not in genres:
            # Copy to drama folder
            if drama_count < 2000:
                shutil.copy2(os.path.join('D:/dequi/Documents/mmimdb.tar/mmimdb/mmimdb/dataset', filename), target_dir)
                shutil.copy2(json_path, target_dir)
                drama_count += 1
                print(f'drama count: {drama_count}')
        elif 'Horror' in genres and 'Drama' not in genres:
            # Copy to horror folder
            if horror_count < 2000:
                shutil.copy2(os.path.join('D:/dequi/Documents/mmimdb.tar/mmimdb/mmimdb/dataset', filename), target_dir)
                shutil.copy2(json_path, target_dir)
                horror_count += 1
                print(f'horror count: {horror_count}')

        # Stop if we have enough images for both genres
        if drama_count >= 2000 and horror_count >= 2000:
            break