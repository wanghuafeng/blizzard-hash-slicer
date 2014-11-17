#encoding:utf-8
from flask import Flask
from flask import Response, request
from slicer import SlicerBase
import simplejson

app = Flask(__name__)

slicebase = SlicerBase()

def to_unicode(sentence):
    sentence = sentence.strip()
    if isinstance(sentence, str):
        try:
            sentence = sentence.decode('utf-8')
        except Exception,e:
            try:
                sentence = sentence.decode('gbk')
            except Exception:
                raise ValueError('unknown coding...')
    return sentence
def to_utf8(sentence):
    sentence = sentence.strip()
    if isinstance(sentence, unicode):
        sentence = sentence.encode('utf-8', 'ignore')
    return sentence
@app.route('/<sentence>',methods=['GET', 'POST'])
def slicer_services(sentence):
    sentence = to_utf8(sentence)
    splied_words_list = slicebase.slice(sentence)
    return simplejson.dumps(splied_words_list)

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')