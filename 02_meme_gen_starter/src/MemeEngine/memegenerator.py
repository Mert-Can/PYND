from PIL import Image, ImageDraw, ImageFont
from random import randint

"""This is the memegenerator module
    This module includes a class MemeEngine that defines 
    a MemeEngine object which contains an output_dir field,
    to store mememified images.
    The class MemeEngine also contains methods:

    1. url_tostring : that converts a HttpRespons object to a string
    2. check_path: extracts raw form of an HttpResponse object 
    3. make_meme: reads in an image, transforms and adds a caption
                  to the image (body and author)

    Example:

    meme = MemeEngine("./output_dir")

    output_path = meme.make_meme("path to image", "body of quote", "author of quote")

    The output_path is the that path to the saved image which has been mememified
"""

class MemeEngine:
    def __init__(self, output_dir):
        self.output_dir = output_dir
    
    def url_tostring(self, url):

        """
        This method checks if 
        """

        if isinstance(url, str):
            return url
        else:
            return url.url

    def check_path(self, path):
        if isinstance(path, str):
            return path
        else:
            return path.raw


    def make_meme(self, img_path, body, author, width=500):

        """This is the make_meme method
        This method reads in an image path using the Pillow library,
        transforms the image by resizing to a maximum width of 500px and
        while maintaining the input aspect ratio.

        It reads in a quote body and author and add as a caption
        to a random location of the images and saves the image.

        Parametes:
        img_path: str or Httpresponse Object (Path to image location)
        body: str (Body text for  a quote)
        author: str (Name of author of a quote)
        width: int (maximum image width, defaut to 500px)

        return:
        output_path: str (Generated image path)
        
        """
        
        img = Image.open(self.check_path(img_path)) # Reads in image_path

        # Resize image
        wpercent = (width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width, hsize), Image.ANTIALIAS)

        # Import a font type and set size
        shadowcolor = 'white'
        fillcolor = 'black'
        fnt = ImageFont.truetype(font='./Adventure.otf', size=24)

        # Write unto image
        d = ImageDraw.Draw(img)
        x, y = randint(10, 200), randint(10, 200)

        # draw border over body
        d.text((x-1, y), body, font=fnt, fill=shadowcolor)
        d.text((x+1, y), body, font=fnt, fill=shadowcolor)
        d.text((x, y-1), body, font=fnt, fill=shadowcolor)
        d.text((x, y+1), body, font=fnt, fill=shadowcolor)

        # draw over body
        d.text((x,y), body, font= fnt, fill=fillcolor )
        
        # draw border over author
        d.text((x-1, y+25), ' - ' + author, font=fnt, fill=shadowcolor)
        d.text((x+1, y+25), ' - ' + author, font=fnt, fill=shadowcolor)
        d.text((x, y+24), ' - ' + author, font=fnt, fill=shadowcolor)
        d.text((x, y+26), ' - ' + author, font=fnt, fill=shadowcolor)
        # draw over author
        d.text((x, y+25), ' - ' + author, font=fnt, fill=fillcolor)

        img_name = self.url_tostring(img_path) # Get image path as string

        img_name = img_name.split('/')[-1].split('.')[0] # extract image name 
        
        output_path = self.output_dir + '/' + img_name # add image name to output_dir 

        img.save(output_path, format='JPEG') # Save image in output_path

        return output_path

