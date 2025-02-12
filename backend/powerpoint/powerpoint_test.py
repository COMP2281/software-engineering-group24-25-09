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

# Creation of slides
def create_slide(name, titleName, content, picture_path):
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[7]  # Choose an appropriate layout
    slide = prs.slides.add_slide(title_slide_layout)

    # Add Title
    title = slide.shapes.title
    if title:
        title.text = titleName

    # Add Content
    if len(slide.placeholders) > 1:
        subtitle = slide.placeholders[1]
        subtitle.text = content

    # Add Picture
    left = Inches(2)  # X position
    top = Inches(2)   # Y position
    width = Inches(4)  # Optional: Set width (height auto-adjusts)

    try:
        slide.shapes.add_picture(picture_path, left, top, width=width)
    except FileNotFoundError:
        print(f"Image file '{picture_path}' not found!")

    prs.save(name)
    print(f"Presentation saved as {name}")

# PowerPoint creation
create_slide("test.pptx", "Test", "Content would be here Why bullet points", "test.png")
