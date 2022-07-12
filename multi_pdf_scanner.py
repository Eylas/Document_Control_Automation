from typing import OrderedDict
# from matplotlib.pyplot import draw
import pdfplumber
import time
import re
import os
import pandas as pd

# metrics
start = time.time()

file_list = []

def get_file_paths(dir):
    for path in os.listdir(dir):
        full_path = os.path.join(dir, path)
        if os.path.isfile(full_path):
            file_list.append(full_path)

get_file_paths(r'C:\Users\Nathan\Documents\Py\PDF_Scanner\loading_area')

# For each file in the file list, search the PDF for the matching document number, if it finds it, return it to a list

basename_list = []
drawing_list = []
rev_list = []
all_drawings = OrderedDict()

dict_number_list = [] 
dict_revision_list = []

# rev_matches = []
# drawing_matches = []

bnl_loop = 0
plumber_loop = 0
dwg_loop = 0
rev_loop = 0
dict_loop = 0

for file in file_list:
        name = os.path.basename(file)
        basename_list.append(name)
        bnl_loop += 1
        print(f"working on {name}")
        # print(f" printing BNL loop: {bnl_loop}")
        with pdfplumber.open(file) as pdf:
            # PDF parsing - for each page of the PDF, crop it to the bottom 25%, extract text
            pages = pdf.pages
            for page in (pages):
                bottom = page.crop((0, 0.85 *float(page.height), page.width, page.height))
                bottom_right = bottom.crop((0.75 * float(bottom.width), 0, bottom.width, bottom.height), relative=True)
                page_text = bottom_right.extract_text(layout=True)
               
                # regex searching for the drawing number
                drawing_pattern = re.compile(r'\w\d\d\d.\w\w\w.\w\w.\w\w\w.\d\d\d.\d\d\d\d\d\d')
                drawing_matches = drawing_pattern.finditer(page_text)

                # revision pattern
                rev_pattern = re.compile(r'P\d\d') 
                rev_matches = rev_pattern.finditer(page_text)
                plumber_loop += 1
                print(f"drawing matches {drawing_list, type(drawing_list), type(drawing_matches)}")
                print(f"rev matches {rev_list, type(rev_list), type(rev_matches)}")
                # generate ordered lists
                for drawing, rev in zip(drawing_matches, rev_matches):
                    drawing_list.append(drawing)
                    rev_list.append(rev)
                
                for name, drawing, rev in zip(basename_list, drawing_list, rev_list):
                        all_drawings[name] = [drawing, rev]
                        
data = pd.DataFrame.from_dict(all_drawings)
data = data.transpose()
dest = 'C:\\Users\\Nathan\\Documents\\Py\\PDF_Scanner\output.csv'
data.to_csv(path_or_buf=dest)
end = time.time()
delta = end-start
print(f"This took {int(delta)} seconds")

# print(f"{basename_list}\n")
print(f"{drawing_list}\n")
# print(f"{rev_list}\n")

# print(all_drawings)
print(f"here is the data \n{data}\n")

# print(f"This loop cycled {bnl_loop} times\n")
# print(f"This loop cycled {plumber_loop} times\n")
# print(f"This loop cycled {dwg_loop} times\n")
# print(f"This loop cycled {rev_loop} times\n")
# print(f"This loop cycled {dict_loop} times\n")


# # your data here
# docs = [...]
# numbers = [...]
# revs = [...]

# output = {}
# for doc, number, rev in zip(docs, numbers, revs):
#     output[doc] = {"number": number, "rev": rev}