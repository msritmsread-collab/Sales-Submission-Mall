import os

def compare_files(file_path1, file_path2):
    with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
        return file1.read() == file2.read()

# Define the two directories
folder1 = 'C:/Users/USER/msread.com.my/TMI-DATA - Documents/Python/Sales Submission Mall/ASP'
folder2 = 'C:/Users/USER/msread.com.my/TMI-DATA - Documents/Python/Sales Submission Mall/ASP_Old'

# Get all file names from folder1
file_names = [f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))]

# Loop through the list of filenames and compare the files from both directories
for file_name in file_names:
    file_path1 = os.path.join(folder1, file_name)
    file_path2 = os.path.join(folder2, file_name)

    if os.path.exists(file_path1) and os.path.exists(file_path2):
        if compare_files(file_path1, file_path2):
            print(f"The files {file_name} match.")
        else:
            print(f"The files {file_name} do not match.")
    else:
        print(f"One or both files named {file_name} do not exist.")