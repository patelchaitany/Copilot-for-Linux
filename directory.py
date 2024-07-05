import os
from termcolor import colored

include = [".pdf"]


def get_size(fiel):
    try:
        size = os.path.getsize(fiel)
        return size / (1024 * 1024)
    except Exception as e:
        print(e)
        print(colored("! Error", "red"))
        return 100000000


def save_directory_structure(root, output_file):
    with open(output_file, "w") as f:
        for dirpath, dirname, filenames in os.walk(root):
            for filename in filenames:
                if any(filename.endswith(ext) for ext in include):
                    f.write(f"{os.path.join(dirpath, filename)}")
                    f.write("\n")


def copy_dir(project_dir, file1, file2):
    with open(f"{project_dir}/{file2}", "r") as f2:
        file2_lines = f2.readlines()

    with open(f"{project_dir}/{file1}", "w") as f1:
        for i in file2_lines:
            f1.write(f"{i}")


def compare_file(dir, project_dir, file1, file2):
    save_directory_structure(dir, f"{project_dir}/{file2}")
    with open(f"{project_dir}/{file1}", "r") as f1, open(
        f"{project_dir}/{file2}", "r"
    ) as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

    rmove_file = []
    for line in file1_lines:
        if line not in file2_lines:
            rmove_file.append(line)

    add_file = []
    for line in file2_lines:
        if line not in file1_lines:
            add_file.append(line)

    return rmove_file, add_file, file1_lines, file2_lines
