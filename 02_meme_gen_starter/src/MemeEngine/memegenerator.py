from PIL import Image, ImageDraw, ImageFont
import os

class MemeEngine:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def make_meme(self, img_path, body, author, width=500):

        img = Image.open(img_path)

        wpercent = (width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width, hsize), Image.ANTIALIAS)

        fnt = ImageFont.truetype(font='./Reglisse.otf', size=20)

        d = ImageDraw.Draw(img)
        d.text((10,10), body + ' - ' + author, font= fnt, fill=(255,255,255) )

        img_name = img_path.split('/')[-1]
        output_path = self.output_dir + '/' + img_name

        img.save(output_path, format='JPEG')

        return output_path

