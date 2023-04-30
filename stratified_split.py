import os
import shutil
import json

train_dir = 'D:/dequi/Documents/mmimdb_train' # 60% : 1200 each horror and drama
valid_dir = 'D:/dequi/Documents/mmimdb_valid' # 20% : 400 each horror and drama
test_dir = 'D:/dequi/Documents/mmimdb_test' # 20% : 400 each horror and drama

dataset_dir = 'D:/dequi/Documents/mmimdb_horror_2000_drama_2000'

train_drama_count = 0
train_horror_count = 0
valid_drama_count = 0
valid_horror_count = 0
test_drama_count = 0
test_horror_count = 0

# Iterate over the files in the dataset folder
i=0
for filename in os.listdir('D:/dequi/Documents/mmimdb_horror_2000_drama_2000'):
    if filename.endswith('.jpeg'):
        # Get the corresponding JSON filename
        json_filename = os.path.splitext(filename)[0] + '.json'
        json_path = os.path.join(dataset_dir, json_filename)

        # Load the JSON file
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Check the genres attribute
        genres = data['genres']
        if 'Drama' in genres and 'Horror' not in genres:
            # Copy to drama folder
            if train_drama_count < 1200:
                shutil.copy2(os.path.join(dataset_dir, filename), f'{train_dir}/drama')
                train_drama_count += 1
                print(f'train drama count: {train_drama_count}')
            # Copy to drama folder
            elif valid_drama_count < 400:
                shutil.copy2(os.path.join(dataset_dir, filename), f'{valid_dir}/drama')
                valid_drama_count += 1
                print(f'valid drama count: {valid_drama_count}')
            # Copy to drama folder
            elif test_drama_count < 400:
                shutil.copy2(os.path.join(dataset_dir, filename), f'{test_dir}/drama')
                test_drama_count += 1
                print(f'test drama count: {test_drama_count}')
        
        elif 'Horror' in genres and 'Drama' not in genres:
            # Copy to horror folder
            if train_horror_count < 1200:
                shutil.copy2(os.path.join(dataset_dir, filename), f'{train_dir}/horror')
                train_horror_count += 1
                print(f'train horror count: {train_horror_count}')
            # Copy to horror folder
            elif valid_horror_count < 400:
                shutil.copy2(os.path.join(dataset_dir, filename), f'{valid_dir}/horror')
                valid_horror_count += 1
                print(f'valid horror count: {valid_horror_count}')
            # Copy to horror folder
            elif test_horror_count < 400:
                shutil.copy2(os.path.join(dataset_dir, filename), f'{test_dir}/horror')
                test_horror_count += 1
                print(f'test horror count: {test_horror_count}')

        i+=1
        print(i, train_drama_count, train_horror_count, valid_drama_count, valid_horror_count, test_drama_count, test_horror_count)
