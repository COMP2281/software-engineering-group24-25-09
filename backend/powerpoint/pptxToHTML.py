# yes this code isnt up to standard Maks. 
# im just getting it to work first
# its a proof of concept

# import library. found at https://docs.aspose.com/slides/python-net/installation/
# Instantiate a Presentation object that represents a presentation file
import aspose.slides as slides

def first_option():
    #pres = slides.Presentation(r'backend\powerpoint\created_slides\new-file-name.pptx')

    pres = slides.Presentation(r'C:\Users\rosie\OneDrive\Documents\2nd Year\Software Engineering\Here is a Title.pptx')

    controller = slides.export.ResponsiveHtmlController()
    htmlOptions = slides.export.HtmlOptions()
    htmlOptions.html_formatter = slides.export.HtmlFormatter.create_custom_formatter(controller)

    # Saving the presentation to HTML
    pres.save("backend\powerpoint\created_slides\PresentationToHTML_out.html", slides.export.SaveFormat.HTML, htmlOptions)

def second_option():
    # this relies of the nuget .net library PPTXToHTML version 1.0.5
    # youtube video here: https://www.youtube.com/watch?v=WaKJAOTLCQw
    # ignore, this is for c sharp . smh smh
    return