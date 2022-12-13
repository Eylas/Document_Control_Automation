import pdfplumber
import time
import re
import os
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
import concurrent.futures
import json

start = time.time()
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
            bottom = page.crop((0, 0.85 *float(page.height), page.width, page.height))
            # fix bottom_right - causing a persistent error when used
            # bottom_right = bottom.crop((0.75 * float(bottom.width), 0, bottom.width, bottom.height), relative=True)
            page_text = bottom.extract_text(layout=True)

            dwg_num = dwg_pattern.search(page_text)
            rev_num = rev_pattern.search(page_text)
            page_num = page.page_number

            # review loop to find out why the json output isnt including all 
            file_dict["Originating_Document"] = get_basename(file)
            file_dict["Originating_Page"] = page_num
            file_dict["Document_Number"] = dwg_num.group(0)
            file_dict["Document_Revision"] = rev_num.group(0)
            print(file_dict)
            file_matches.append(file_dict)

            page.flush_cache()
            page.get_text_layout.cache_clear()
    with open('report_outputfile.json', 'w') as fout:
        json.dump(file_matches, fout, indent=4)
    return file_matches
                
    
# Function executions

file_list = get_file_paths(path)
print(f'The number of files to scan is:  {counter(file_list)}\n')


if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor() as executor:
        start_time = time.perf_counter()
        result = list(executor.map(pdf_mapper, file_list))
        finish_time = time.perf_counter()
        with open('report_out.json', 'w') as fout:
            json.dump(result, fout, indent=4)
        print(f"Program finishIed in {finish_time-start_time} seconds")