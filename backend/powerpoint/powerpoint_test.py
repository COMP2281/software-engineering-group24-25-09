# Could implement adding your own slides to the application
# Has to be on powerpoints from 2007 onwards
# So the powerpoints in terms of what John sent up were in this order in terms of the layouts on powerpoint
# Pick a colour that will be set as the background for all the slides can be done but creating a shape and just filling the backgrounf with it 
# 1. Title only (Could be the engagment title)
# 2. Title slide with text could be info about the engagments
# 3. Caption and image
# 4. Lots of caption with images but sometimes a title slide.

# Flow of user
# 1. Choose an engagment
# 2. Make a single slide
# 3. Collect which slides I want to use in slide show
# 4. Export full powerpoint

from pptx import Presentation
from pptx.util import Inches
import os
import random
TEMPLATES = os.getenv("TEMPLATES", "templates") # Gets the path to the files
TEMPLATE_LIST = os.listdir(TEMPLATES) # Gets the files in the location

# From Existing temples create a slide
def create_slide(export_name, title_name, text, content):
    # Select a random template created
    selected_item = random.choice(TEMPLATE_LIST)

    # Open that slide
    os.chdir("templates")
    prs = Presentation(selected_item)
    slide = prs.slides[0]
    os.chdir("..")

    for shape in slide.placeholders:
        print('%d %s' % (shape.placeholder_format.idx, shape.name))
        shape_format = shape.placeholder_format
        shape_type = str(shape_format.type).split(' (')[0]
        shape_index = shape.placeholder_format.idx
        placeholder = slide.placeholders[shape_index]

        # Change title 
        if shape_type == "TITLE":
            print("TITLE FOUND")
            placeholder.text = title_name


        # Change text
        if shape_type == "BODY":
            print("TEXT BOX FOUND")
            placeholder.text = text     

        # Change content
        if shape_type == "OBJECT":
            print("CONTENT BOX FOUND")
            


    # Save the changed slide
    os.chdir("created_slides")
    prs.save('new-file-name.pptx')
    os.chdir("..")


# Group the slides together
def export_powerpoint():
    pass

# PowerPoint creation
create_slide("test.pptx", "Test", "Content would be here Why bullet points", "test.png")
