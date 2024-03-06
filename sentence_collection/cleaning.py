import os
import re

# Assign directory that contains the files to be cleaned
directory = "path/to/directory"

# Iterate over files in that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    
    # Checking if it is a file
    if os.path.isfile(f):
        print(f)
        new_filename = filename[:-4]
        
        # Open file
        with open(f, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Remove all characters before the first letter in each line
        cleaned_lines = [re.sub(r'^[^a-zA-Z]*', '', line) for line in lines]

        # Save the cleaned-up content back to the file
        with open(f'cleaned_{new_filename}.txt', 'w', encoding='utf-8') as file:
            file.write(''.join(cleaned_lines))

        print(f"Cleaned-up content saved to cleaned_{new_filename}.txt.")
