from pydantic.v1 import parse
from directory import save_directory_structure, compare_file, copy_dir, get_size
from embeding import get_embd, get_query, process, delete, create_db
import os
from pathlib import Path
import chromadb
from termcolor import colored
from tqdm import tqdm
import argparse


def main(size):
    root_dir = os.path.expanduser("~")
    current_dir = os.getcwd()
    include = [".pdf"]
    error_pdf = []
    succse_pdf = []
    print(Path(f"{current_dir}/output.txt").exists())
    if not Path(f"{current_dir}/output.txt").exists():
        # create_db()
        save_directory_structure(root_dir, f"{current_dir}/t_output.txt")
        remove_file, add_file, past_dir, new_dir = compare_file(
            root_dir, current_dir, "t_output.txt", "output.txt"
        )
        for i in tqdm(past_dir, desc="Processing files"):
            i = str(i).replace("\n", "")
            if any(str(i).endswith(ext) for ext in include) and get_size(i) <= size:
                error = process(i)
                if error:
                    # print(colored(f"Error file {i}", "red"))
                    error_pdf.append(i)
                else:
                    # print(colored(f"{i}", "green"))
                    succse_pdf.append(i)
        with open(f"{current_dir}/t_output.txt", "w") as f:
            for i in succse_pdf:
                f.write(i)
                f.write("\n")
        copy_dir(current_dir, "output.txt", "t_output.txt")

    else:
        remove_file, add_file, past_dir, new_dir = compare_file(
            root_dir, current_dir, "output.txt", "n_output.txt"
        )
        for i in tqdm(remove_file, desc="Removing Old File Data"):
            i = str(i).replace("\n", "")
            delete(i)

        for i in tqdm(add_file, desc="Adding New File data"):
            i = str(i).replace("\n", "")
            if get_size(i) > size:
                error_pdf.append(i)
                continue
            error = process(i)
            if error:
                print(colored(f"Error file {i}", "red"))
                error_pdf.append(i)
            else:
                print(colored(f"{i}", "green"))
                succse_pdf.append(i)

        with open(f"{current_dir}/output.txt", "w") as f:
            for i in new_dir:
                i = str(i).replace("\n", "")
                if i not in error_pdf and get_size(i) <= size:
                    f.write(i)
                    f.write("\n")

    if len(add_file):
        print("Parsed This files\n")
        for i in succse_pdf:
            print(colored(f"{i}", "green"))

    q = input("Word need to serch in document : ")
    doc = get_query(q)
    ans = set()

    for i in doc:
        ind = str(i).find(":")
        ans.add(i[:ind])
    print()
    print(ans)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument(
        "--size", type=int, default=5, help="Maximum size of files to process (in MB)"
    )
    args = parser.parse_args()

    main(args.size)
