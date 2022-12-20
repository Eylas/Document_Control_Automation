import pdfplumber
from wand.image import Image
from wand.display import display
import re
import os


def image_print(name, img):
    img = img.to_image(resolution=150)
    img.save(
        f"img_page_number_{img.page.page_number}_{name}.png", format="PNG")

# with pdfplumber.open(r'C:\Users\Natha\Document_Control_Automation\loading_area\C321-MMD-RT-DPP-130-591702.pdf') as pdf:
#     for page in pdf.pages:

#         # x0, starting
#         # top, top to bottom
#         # x1, ending
#         # bottom, bottom to top

#         crops = {
#             "bottom": page.crop((0, 0.85 *float(page.height), page.width, page.height)),
#             "bottom_right": page.crop((0.85 *float(page.width), 0.85 *float(page.height), page.width, page.height)),
#             "bottom_left": page.crop((0, 0.85 *float(page.height), 0.15 *float(page.width), page.height)),

#             "top": page.crop((0, 0.,page.width, 0.15 *float(page.height))),
#             "top_right": page.crop((0.85 *float(page.width), 0, page.width, 0.15 *float(page.height))),
#             "top_left": page.crop((0, 0, 0.15 *float(page.width), 0.15 *float(page.height)))
#         }

#         for crop, img in crops.items():
#             image_print(crop, img)


dwg_pattern = re.compile(r'\w\d\d\d.\w\w\w.\w\w.\w\w\w.\d\d\d.\d\d\d\d\d\d')
rev_pattern = re.compile(r'P\d\d')

path = r'C:\Users\Natha\Document_Control_Automation\loading_area'


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


def drawing_crop_selector():

    options = ['Bottom', 'Bottom left',
               'Bottom right', 'Top', 'Top right', 'Top left']
    user_input = ""
    input_message = "Please select crop area to localise the data you want to extract:\n"

    for index, item in enumerate(options):
        input_message += f"{index+1}) {item}\n"

    input_message += "Your selection: "

    while user_input.capitalize() not in options:
        user_input = input(input_message)
    print("You selected: " + user_input)
    return user_input


selection = drawing_crop_selector()


def pdf_mapper(file):
    file_matches = []

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            file_dict = {"Originating_Document": [],
                         "Originating_Page": [],
                         "Document_Number": [],
                         "Document_Revision": []}

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

            print(f"Currently working on {get_basename(file)}")
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


file_list = get_file_paths(path)

for file in file_list:
    pdf_mapper(file)
