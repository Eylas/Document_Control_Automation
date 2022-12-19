import pdfplumber
from wand.image import Image
from wand.display import display
import re
import os

def image_print(name, img):
    img = img.to_image(resolution=150)
    img.save(f"img_page_number_{img.page.page_number}_{name}.png", format="PNG")

with pdfplumber.open(r'C:\Users\Natha\Document_Control_Automation\loading_area\C321-MMD-RT-DPP-130-591702.pdf') as pdf:
    for page in pdf.pages:

        # x0, starting
        # top, top to bottom
        # x1, ending
        # bottom, bottom to top

        crops = {
            "bottom": page.crop((0, 0.85 *float(page.height), page.width, page.height)),
            "bottom_right": page.crop((0.85 *float(page.width), 0.85 *float(page.height), page.width, page.height)),
            "bottom_left": page.crop((0, 0.85 *float(page.height), 0.15 *float(page.width), page.height)),

            "top": page.crop((0, 0.,page.width, 0.15 *float(page.height))),
            "top_right": page.crop((0.85 *float(page.width), 0, page.width, 0.15 *float(page.height))),
            "top_left": page.crop((0, 0, 0.15 *float(page.width), 0.15 *float(page.height)))
        }

        for crop, img in crops.items():
            image_print(crop, img)
        
dwg_pattern = re.compile(r'\w\d\d\d.\w\w\w.\w\w.\w\w\w.\d\d\d.\d\d\d\d\d\d')
rev_pattern = re.compile(r'P\d\d') 

path = r'C:\Users\Natha\Document_Control_Automation\loading_area'