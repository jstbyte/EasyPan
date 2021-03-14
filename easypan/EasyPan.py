from PIL import Image, ImageDraw, ImageFont
from sys import argv
import os
import json

COMPONENTS_DIR = os.path.dirname(argv[0]) + '\\components\\'
BOX_WIDTH = 59


class FormData():
    title = ''
    first_name = ''
    last_name = ''
    fa_firstname = ''
    fa_lastname = ''
    dob = ''
    house = ''
    village = ''
    post = ''
    dist = ''
    state = ''
    pin = ''

    def parse_easy_pan_form(self, jdata: dict):
        self.title = jdata.get('ApplicantTitle', '').replace('string:', '')
        self.first_name = jdata.get('firstname', '')
        self.last_name = jdata.get('lastname', '')
        self.fa_firstname = jdata.get('father_firstname', '')
        self.fa_lastname = jdata.get('father_lastname', '')
        self.dob = jdata.get('dob', '')
        self.house = jdata.get('c_houseno', '')
        self.village = jdata.get('c_village', '')
        self.post = jdata.get('c_post', '')
        self.dist = jdata.get('c_District', '')
        self.state = jdata.get('c_State', '')
        self.pin = jdata.get('c_PIN', '')


def write_text(text:str, x:int, y:int, drawable):
    myFont = ImageFont.truetype(COMPONENTS_DIR + 'Menlo-Regular.ttf', 50)
    for char in text.upper():
        drawable.text((x, y), char, font=myFont, fill =(0, 0, 0))
        x = x + BOX_WIDTH

def write_text_linier(text:str, x:int, y:int, drawable):
    myFont = ImageFont.truetype(COMPONENTS_DIR + 'Menlo-Regular.ttf', 50)
    drawable.text((x, y), text, font=myFont, fill =(0, 0, 0))

def write_form(data:FormData):
    img:Image.Image = Image.open(COMPONENTS_DIR + 'F49A.jpg')
    yes = Image.open(COMPONENTS_DIR + 'yes.png')

    canvas = ImageDraw.Draw(img)
    
    write_text(data.last_name, 758, 868, canvas) # last_name;
    write_text(data.first_name, 758, 868 + BOX_WIDTH + 6, canvas) # first_name;

    write_text(data.first_name + ' ' + data.last_name, 148, 1130, canvas) # to_printed;

    dob = data.dob.split('/')
    write_text(dob[0], 148, 1820, canvas) # DD;
    write_text(dob[1], 325, 1820, canvas) # MM;
    write_text(dob[2], 500, 1820, canvas) # YYYY;

    write_text(data.fa_lastname, 760, 2150, canvas) # father_lastname;
    write_text(data.fa_firstname, 760, 2215, canvas) # father_firstname;
    img.paste(yes.copy(), (140, 2625), yes)

    if ( data.title.upper() == 'SHRI' ):
        img.paste(yes.copy(), (755, 810), yes) # Title;
        img.paste(yes.copy(), (832, 1645), yes) # Gender;

    elif ( data.title.upper() == 'SMT.' ):
        img.paste(yes.copy(), (975, 810), yes) # Title;
        img.paste(yes.copy(), (1065, 1645), yes) # Gender;

    elif ( data.title.upper() == 'KUMARI' ):
        img.paste(yes.copy(), (1185, 810), yes)
        img.paste(yes.copy(), (1065, 1645), yes) # Gender;

    write_text(data.house, 760, 2885, canvas) # House No;
    write_text(data.village, 760, 2948, canvas) # Village Name;
    write_text(data.village, 760, 3008, canvas) # Post Office;
    write_text(data.dist, 760, 3135, canvas) # District;
    write_text_linier('ASSAM', 450, 3265, canvas) # State;
    write_text(data.pin, 970, 3265, canvas) # State;
    write_text_linier('INDIA', 1670, 3265, canvas) # State;

    path = os.path.dirname(argv[1])
    if path:
        path = path + '/'
    img.save(f'{path}{data.first_name}_{data.last_name}.jpg')



if __name__ == '__main__':
    file = open(argv[1])
    data = FormData()
    data.parse_easy_pan_form(json.loads( file.read() ))
    file.close()
    write_form(data)