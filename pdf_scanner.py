import pdfplumber
import time
import re
import os
import concurrent.futures
import json
import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


path = r'C:\Users\Natha\Document_Control_Automation\loading_area'

# regex patterns
dwg_pattern = re.compile(r'\w\d\d\d.\w\w\w.\w\w.\w\w\w.\d\d\d.\d\d\d\d\d\d')
rev_pattern = re.compile(r'P\d\d')

# Functions


def get_file_paths(dir):
    file_list = []
    for path in os.listdir(dir):
        full_path = os.path.join(dir, path)
        if os.path.isfile(full_path):
            file_list.append(full_path)
    return file_list


def get_basename(path):
    file_name = os.path.basename(path)
    return file_name


def askdirectory():
    dirname = filedialog.askdirectory()
    print(dirname)
    return (dirname)

def drawing_crop_selector():

    options = [
        'Bottom', 'Bottom left', 'Bottom right', 'Top', 'Top right', 'Top left'
    ]

    user_input = ""
    input_message = "Please select crop area to localise the data you want to extract:\n"

    for index, item in enumerate(options):
        input_message += f"{index+1}) {item}\n"

    input_message += "Your selection: "

    while user_input.capitalize() not in options:
        user_input = input(input_message)
    print("You selected: " + user_input)
    return user_input


def get_file_paths(dir):
    file_list = []
    for path in os.listdir(dir):
        full_path = os.path.join(dir, path)
        if os.path.isfile(full_path):
            file_list.append(full_path)
    return file_list


def get_basename(path):
    file_name = os.path.basename(path)
    return file_name


def pdf_mapper(file):
    file_matches = []
    selection = drawing_crop_selector()
    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:
            print(f"Currently working on {get_basename(file)}\n")

            file_dict = {
                "Originating_Document": [],
                "Originating_Page": [],
                "Document_Number": [],
                "Document_Revision": []
            }

            def pdf_cropper(selection):
                match selection:
                    case "Bottom":
                        bottom_selected = page.crop(
                            (0, 0.85 * float(page.height), page.width, page.height))
                        return bottom_selected
                    case "Bottom right":
                        bottom_right_selected = page.crop(
                            (0.85 * float(page.width), 0.85 * float(page.height), page.width, page.height))
                        return bottom_right_selected
                    case "Bottom left":
                        bottom_left_selected = page.crop(
                            (0, 0.85 * float(page.height), 0.15 * float(page.width), page.height))
                        return bottom_left_selected
                    case "Top":
                        top_selected = page.crop(
                            (0, 0., page.width, 0.15 * float(page.height)))
                        return top_selected
                    case "Top right":
                        top_right_selected = page.crop(
                            (0.85 * float(page.width), 0, page.width, 0.15 * float(page.height)))
                        return top_right_selected
                    case "Top left":
                        top_left_selected = page.crop(
                            (0, 0, 0.15 * float(page.width), 0.15 * float(page.height)))
                        return top_left_selected

            cropping = pdf_cropper(selection)
            page_text = cropping.extract_text(layout=True)
            print(page_text)

            dwg_num = dwg_pattern.search(page_text)
            rev_num = rev_pattern.search(page_text)
            page_num = page.page_number

            file_dict["Originating_Document"] = get_basename(file)
            file_dict["Originating_Page"] = page_num
            file_dict["Document_Number"] = dwg_num.group(0)
            file_dict["Document_Revision"] = rev_num.group(0)
            file_matches.append(file_dict)

            page.flush_cache()
            page.get_text_layout.cache_clear()

    return file_matches


def report_output(data, name):
    with open(f'{name}.json', 'w') as fout:
        json.dump(data, fout, indent=4)
    return data


# Function executions
file_list = get_file_paths(path)
for file in file_list:
    pdf_mapper(file)

# if __name__ == "__main__":
#     file_list = get_file_paths(path)
#     start_time = time.perf_counter()

#     result = {}
#     selection = drawing_crop_selector()
#     with concurrent.futures.ProcessPoolExecutor(4) as executor:
#         result = list(executor.map(pdf_mapper, file_list))

#         report_output(result, 'report_output')
#         finish_time = time.perf_counter()

#     print(f"Program finishIed in {finish_time-start_time} seconds")
