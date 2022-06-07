#--Importing Packages

import os
from flask import Flask, request
import base64
import cv2
import easyocr
from deep_translator import GoogleTranslator as gt
from flask_cors import CORS


app = Flask(__name__, static_url_path='')
cors = CORS(app)


@app.route('/', methods = ['POST'])
def upload_page():

    #fething data from App

    data = request.get_json()
    img = data['image']
    img = img.split(',')[1]
    with open('image.jpg','wb') as f:
        print(f.write(base64.b64decode(img)))

    imfile = cv2.imread('image.jpg')
    print(type(imfile))

    # storing the language parameters 

    source = data['source']
    target = data['target']
    computation = getText(source, target, imfile)
    extraction = computation[0]
    translation = computation[1]
    send = {"extract":extraction, "translate":translation}
    os.remove('image.jpg')
    return send
       

def getText(source, target, imfile):

    tsource = source  
    ttarget = target 
    imge = imfile
    print(type(imge), tsource, ttarget)

    reader = easyocr.Reader([tsource], gpu = False, model_storage_directory = os.getcwd())
    result = reader.readtext(getImage(imge), detail = 0, paragraph = True)
    text = " ".join(result)
    
    transText = gt(source = tsource, target = ttarget).translate(text)
    finalVal = [text, transText]
    print(finalVal[0])

    return finalVal  


def getImage(imfile):

    rgb = cv2.cvtColor(imfile, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.bitwise_not(gray)

    #-- scaled if width is less

    width = gray.shape[1]
    if width < 350: 
     gray = cv2.resize(gray, (520, 350))
     print("Scaled")

    return gray


if __name__ == '__main__':
    app.debug = True
    app.run()
