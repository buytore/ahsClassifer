# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 08:37:27 2016

@author: markbannan & Bijan Farhoudi
"""
import os, sys
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))  # Builds directory to script - regardless of OS
UPLOAD_FOLDER =  os.path.join(SCRIPT_FOLDER, 'docs')        # Sets upload directory
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):             # breaks file into file name & extension 
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            newFile = os.path.join(UPLOAD_FOLDER, filename)
            #return redirect(url_for('uploaded_file', filename=filename))
            print "This is the newFile name: ", newFile
            textInfo = convert_pdf_to_txt(newFile)
            write_Text_File(textInfo, filename, ".txt")
            return  '''
                    <!doctype html>
                    <title>Writting Text File</title>
                    <h1>Writting the Text File Out</h1>
                    '''
    
    return  '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=file>
            <input type=submit value=Upload>
            </form>
            '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/writting/<filename>')
def writting_file(filename):
    return '''
    <!doctype html>
    <title>Writting Text File</title>
    <h1>Writting the Text File Out</h1>
    '''
    

############# PDF CONVERTER SECTION ###########################################

def convert_pdf_to_txt(fileToConvert):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    print "Convert_PDF call: ", fileToConvert
    fp = file(fileToConvert, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def write_Text_File(fileContent, fileName, fileExtension='.txt'):
    folder = "text/"
    fileExtension = '.txt'
    newFile = folder + fileName + fileExtension
    f = open(newFile, "w")
    f.write(fileContent)
    f.close()
    return '''
            <!doctype html>
            <title>Writting Text File</title>
            <h1>Writting the Text File Out</h1>
            '''
    

def process_many_files():

    path = os.getcwd()                                  #Get the current directory
    filenames = next(os.walk(path))[2]                  #Get all the files in current directory
    
    for f in filenames:
        filename, file_extension = os.path.splitext(f)
        print "this is the file name: ", filename
        print "this is the file extension: ", file_extension
        if file_extension == ".pdf":      
            textInfo = convert_pdf_to_txt(f)
            write_Text_File(textInfo, filename, file_extension)   
    
# THis is just a test
if __name__ == '__main__':
    app.run()