from PIL import Image, ImageDraw, ImageFont
from sys import argv
import os
import json

COMPONENTS_DIR = os.path.dirname(argv[0]) + '\\components\\' # Use Only 'components\\' while in DevMode;
BOX_WIDTH = 59

PAN_CENTER_PLACE = 'AMBARI BAZAR'


class FormData():
    title = ''
    first_name = ''
    middle_name = ''
    last_name = ''
    card_name = ''
    fa_firstname = ''
    fa_middlename = ''
    fa_lastname = ''
    dob = ''
    house = ''
    village = ''
    post = ''
    dist = ''
    state = ''
    pin = ''
    phone = ''
    email = ''
    aadhaar_num = ''
    aadhaar_name = ''

    def parse_easy_pan_form(self, jdata: dict):
        self.title = jdata.get('ApplicantTitle', '').replace('string:', '')
        self.first_name = jdata.get('firstname', '')
        self.middle_name = jdata.get('middlename', '')
        self.last_name = jdata.get('lastname', '')
        self.card_name = jdata.get('cardname', '')
        self.fa_firstname = jdata.get('father_firstname', '')
        self.fa_middlename = jdata.get('father_middlename', '')
        self.fa_lastname = jdata.get('father_lastname', '')
        self.dob = jdata.get('dob', '')
        self.house = jdata.get('c_houseno', '')
        self.village = jdata.get('c_village', '')
        self.post = jdata.get('c_post', '')
        self.dist = jdata.get('c_District', '')
        self.state = jdata.get('c_State', '')
        self.pin = jdata.get('c_PIN', '')
        self.phone = jdata.get('contactno', '')
        self.email = jdata.get('email', '')
        self.aadhaar_num = jdata.get('Aadhaar_No', '')
        self.aadhaar_name = jdata.get('Aadhaar_name', '')


def write_text(text:str, x:int, y:int, drawable):
    myFont = ImageFont.truetype(COMPONENTS_DIR + 'caveat-regular.ttf', 40)
    for char in text.upper():
        drawable.text((x, y), char, font=myFont, fill =(0, 0, 0))
        x = x + BOX_WIDTH

def write_text_linier(text:str, x:int, y:int, drawable, font_size = 40):
    myFont = ImageFont.truetype(COMPONENTS_DIR + 'caveat-regular.ttf', font_size)
    drawable.text((x, y), text, font=myFont, fill =(0, 0, 0))

def write_form(data:FormData):
    sex = '' # For Next Page;
    img:Image.Image = Image.open(COMPONENTS_DIR + 'F49A.jpg')
    yes = Image.open(COMPONENTS_DIR + 'yes.png')

    canvas = ImageDraw.Draw(img)
    
    write_text(data.last_name, 758, 868, canvas) # last_name;
    write_text(data.first_name, 758, 933, canvas) # first_name;
    write_text(data.middle_name, 758, 995, canvas) # middle_name;

    write_text(data.card_name, 148, 1130, canvas) # card_name;

    dob = data.dob.split('/')
    write_text(dob[0], 148, 1820, canvas) # DD;
    write_text(dob[1], 325, 1820, canvas) # MM;
    write_text(dob[2], 500, 1820, canvas) # YYYY;

    write_text(data.fa_lastname, 760, 2150, canvas) # father_lastname;
    write_text(data.fa_firstname, 760, 2215, canvas) # father_firstname;
    write_text(data.fa_middlename, 760, 2280, canvas) # father_middlename;
    img.paste(yes.copy(), (140, 2625), yes)

    if ( data.title.upper() == 'SHRI' ):
        img.paste(yes.copy(), (755, 810), yes) # Title;
        img.paste(yes.copy(), (832, 1645), yes) # Gender;
        sex = 'male'

    elif ( data.title.upper() == 'SMT.' ):
        img.paste(yes.copy(), (975, 810), yes) # Title;
        img.paste(yes.copy(), (1065, 1645), yes) # Gender;
        sex = 'female'

    elif ( data.title.upper() == 'KUMARI' ):
        img.paste(yes.copy(), (1185, 810), yes)
        img.paste(yes.copy(), (1065, 1645), yes) # Gender;
        sex = 'female'

    write_text(data.house, 760, 2885, canvas) # House No;
    write_text(data.village, 760, 2948, canvas) # Village Name;
    write_text(data.post, 760, 3008, canvas) # Post Office;
    write_text(data.dist, 760, 3135, canvas) # District;
    write_text_linier('ASSAM', 450, 3265, canvas) # State;
    write_text(data.pin, 970, 3265, canvas) # State;
    write_text_linier('INDIA', 1670, 3265, canvas) # State;

    path = os.path.dirname(argv[1])
    if path:
        path = path + '/'
    img.save(f'{path}{data.first_name}_{data.last_name}.jpg')
    img.close()

    """ Code Next Page """
    img = Image.open(COMPONENTS_DIR + 'F49A2.jpg')
    canvas = ImageDraw.Draw(img)

    img.paste(yes.copy(), (980, 530), yes) # Tick Residence;
    write_text('+91', 320, 692, canvas) # Country Code;
    write_text(data.phone, 1030, 692, canvas) # Phone No;
    write_text_linier(data.email, 320, 758, canvas, 40) # Email;
    img.paste(yes.copy(), (140, 955), yes) # Tick Residence;

    if ( data.aadhaar_num and data.aadhaar_name ):
        write_text(data.aadhaar_num, 930, 1255, canvas) # Aadhaar Number;
        write_text(data.aadhaar_name, 750, 1455, canvas) # Aadhaar Name;

    img.paste(yes.copy(), (1795, 1825), yes) # Tick No Income;
    write_text_linier(data.card_name.capitalize(), 220, 3035, canvas, 40) # We/I;

    if (sex == 'male'):
        write_text_linier('Himself', 1730, 3045, canvas, 30) # Himself;
    else:
        write_text_linier('Herself', 1730, 3045, canvas, 30) # Herself;

    write_text_linier(PAN_CENTER_PLACE, 340, 3170, canvas, 30) # PAN Center Place;

    img.save(f'{path}{data.first_name}_{data.last_name}#.jpg')

if __name__ == '__main__':
    file = open(argv[1])
    data = FormData()
    data.parse_easy_pan_form(json.loads( file.read() ))
    file.close()
    write_form(data)