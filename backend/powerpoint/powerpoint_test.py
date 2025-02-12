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
def create_slide(export_name, title_name, content, picture):
    selected_item = random.choice(TEMPLATE_LIST)


# Group the slides together
def export_powerpoint():
    pass

# PowerPoint creation
create_slide("test.pptx", "Test", "Content would be here Why bullet points", "test.png")
