import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
import numpy as np
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import pickle
from sklearn.metrics import precision_score

def convert_pdf_to_txt(fileConvert):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(fileConvert, 'rb')
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
    folder = "uploads/textFiles/"
    fileExtension = '.txt'
    newFile = folder + fileName + fileExtension
    f = open(newFile, "w")
    f.write(fileContent)
    f.close()



UPLOAD_FOLDER = 'C:/Users/bfarhoudi/PycharmProjects/textClassification/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
mainDS = load_files ('pubMed/learn')
testDS = load_files ('pubMed/test')
trainedCLF = pickle.load(open("pickled/trained.p", "rb"))
pr = trainedCLF.predict(testDS.data)
precision = precision_score(testDS.target,pr,average=None).tolist()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filePath = UPLOAD_FOLDER + filename
            write_Text_File(convert_pdf_to_txt(filePath), 'textFile')
            return redirect(url_for('classify',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload the File to identify its content type</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def classify(filename):
    ds = load_files('uploads')
    trainedCLF = pickle.load(open("pickled/trained.p", "rb"))
    predicted = trainedCLF.predict(ds.data)
    message = "The suggested Content Type with " + str(round(precision[predicted[0]]*100)) + " percent pecisionis is: "+mainDS.target_names[predicted[0]]
    return message

if __name__ == '__main__':
    app.run()