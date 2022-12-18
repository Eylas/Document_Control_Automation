import pdfplumber
import time
import re
import os
import concurrent.futures
import json

path = r'C:\Users\Natha\Document_Control_Automation\loading_area'

#regex patterns
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

def counter(list):
    count = 0
    for index, file in enumerate(list):
        count = count + 1
    return count

def pdf_mapper(file):
    file_matches = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            
            file_dict = {"Originating_Document":[], 
            "Originating_Page":[], 
            "Document_Number":[], 
            "Document_Revision":[]}
            
            print(f"Currently working on {get_basename(file)}")
            bottom_right = page.crop((0.85 *float(page.width), 0.85 *float(page.height), page.width, page.height))

            page_text = bottom_right.extract_text(layout=True)
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

def report_output(input, name):
    with open(f'{name}.json', 'w') as fout:
        json.dump(input, fout, indent=4)
    return input 
    
# Function executions

file_list = get_file_paths(path)

for file in file_list:
    pdf_mapper(file)

# if __name__ == "__main__":

#     start_time = time.perf_counter()
#     result = {}
  
#     with concurrent.futures.ProcessPoolExecutor(4) as executor:
#         result = list(executor.map(pdf_mapper, file_list))
        
#         report_output(result,'report_output')
#         finish_time = time.perf_counter()

#     print(f"Program finishIed in {finish_time-start_time} seconds")