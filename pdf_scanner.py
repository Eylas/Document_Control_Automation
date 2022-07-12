import pdfplumber
import time
import re
import os

file_list = []
start = time.time()

#regex
pattern = re.compile(r'\w\d\d\d.\w\w\w.\w\w.\w\w\w.\d\d\d.\d\d\d\d\d\d')
rev_pattern = re.compile(r'P\d\d') 

# run through directory and get absolute path of each file
def get_file_paths(dir):
    for path in os.listdir(dir):
        full_path = os.path.join(dir, path)
        if os.path.isfile(full_path):
            file_list.append(full_path)

def get_basename(path):
    os.path.basename(path)

get_file_paths(r'C:\Users\Nathan\Documents\Py\PDF_Scanner\loading_area')

for file in file_list:
    print(f"Working on file: {file}")
    with pdfplumber.open(file) as pdf:
        page_matches = []
        #pdf parsing to localise the bottom of the page      
        for page in pdf.pages:
            # print(f"Working on page:{}")
            bottom = page.crop((0, 0.85 *float(page.height), page.width, page.height))
            bottom_right = bottom.crop((0.75 * float(bottom.width), 0, bottom.width, bottom.height), relative=True)
            page_text = bottom_right.extract_text(layout=True)
            # print(page_text)
            
            #regex searching for the drawing number and revision pattern
            file_matches = []
            dwg_match = pattern.findall(page_text)
            file_matches.append(dwg_match)
            rev_match = rev_pattern.findall(page_text)
            file_matches.append(rev_match)
            page_matches.append(file_matches)
       
    print(get_basename(file), page_matches)
    #make not get_basename does not work on linux based systems, only windows OS
end = time.time()
delta = end-start
print(delta)