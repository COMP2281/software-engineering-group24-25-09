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
import win32com.client
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
        print(shape_type)
        # Change title 
        if shape_type == "TITLE":
            print("TITLE FOUND")
            placeholder.text = title_name


        # Change text
        elif shape_type == "BODY":
            print("TEXT BOX FOUND")
            placeholder.text = text     

        # Change content
        elif shape_type == "PICTURE":
            print("CONTENT BOX FOUND")
            placeholder.insert_picture(content)

    
    # Save the changed slide
    os.chdir("created_slides")
    prs.save(export_name)
    os.chdir("..")


# Group the slides together
def merge_presentations(presentations, path):
  os.chdir("created_slides")
  ppt_instance = win32com.client.Dispatch('PowerPoint.Application')
  prs = ppt_instance.Presentations.open(os.path.abspath(presentations[0]), True, False, False)

  for i in range(1, len(presentations)):
      prs.Slides.InsertFromFile(os.path.abspath(presentations[i]), prs.Slides.Count)

  prs.SaveAs(os.path.abspath(path))
  prs.Close()


        

# PowerPoint creation
create_slide("test3.pptx", "Test", "Content would be here Why bullet points", "test.png")


merge_presentations(["test2.pptx", "test.pptx", "test3.pptx"],"FINAL.pptx")

