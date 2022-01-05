# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 17:31:20 2021

@author: Frank
"""
import sys
import os
import gensim.downloader
from gensim.models import Word2Vec
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QTextCursor
from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM


class MainWindow(QtWidgets.QDialog):
    textProcessing = Word2Vec()
    buttonList = []
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        uic.loadUi("Schreibhilfe_MainWindow.ui", self)
        self.buttonSynonyms.clicked.connect(self.findSynonyms)
        self.buttonTranslation.clicked.connect(self.translate)        
        self.textProcessing = Textprocessing()
        self.buttonList.append(self.buttonOption1)
        self.buttonList.append(self.buttonOption2)
        self.buttonList.append(self.buttonOption3)
        self.buttonList.append(self.buttonOption4)
        self.buttonList.append(self.buttonOption5)
        self.buttonList.append(self.buttonOption6)
        self.buttonList.append(self.buttonOption7)
        self.buttonList.append(self.buttonOption8)
        self.buttonList.append(self.buttonOption9)
        self.buttonList.append(self.buttonOption10)
        self.buttonOption1.clicked.connect(lambda: self.commitText(self.buttonOption1.text()))
        self.buttonOption2.clicked.connect(lambda: self.commitText(self.buttonOption2.text()))
        self.buttonOption3.clicked.connect(lambda: self.commitText(self.buttonOption3.text()))
        self.buttonOption4.clicked.connect(lambda: self.commitText(self.buttonOption4.text()))
        self.buttonOption5.clicked.connect(lambda: self.commitText(self.buttonOption5.text()))
        self.buttonOption6.clicked.connect(lambda: self.commitText(self.buttonOption6.text()))
        self.buttonOption7.clicked.connect(lambda: self.commitText(self.buttonOption7.text()))
        self.buttonOption8.clicked.connect(lambda: self.commitText(self.buttonOption8.text()))
        self.buttonOption9.clicked.connect(lambda: self.commitText(self.buttonOption9.text()))
        self.buttonOption10.clicked.connect(lambda: self.commitText(self.buttonOption10.text()))
            
    # TODO: implement a 'generate' button, to let the gpt-2 model generate some text    
        
    def translate(self):  
        text = self.textGerman.toPlainText()
        # To avoid that the translated text will be to long for the buttons, the 
        # germanText-field will be used for the output if the input contains more as one word
        if len(text.split(" ")) > 1:
            resultList = self.textProcessing.getTranslation(text, n=1)
            self.textGerman.setText(resultList[0])
        else:
            # number of return values reduced to 5 to increase performance, can be increased to 10 if necessary 
            resultList = self.textProcessing.getTranslation(text, n=5)        
            for index, value in enumerate(resultList):
                if index < 10:
                    self.buttonList[index].setText(value)
        
    def findSynonyms(self):
        cursor = self.textEnglish.textCursor()
        text = ""
        if cursor.selectionStart() == cursor.selectionEnd():
            # if nothing is highlighted use the last word of the text
            text = self.textEnglish.toPlainText().split(" ")[-1]
        else:
            text = cursor.selectedText()
            # check if more as one word is highlighted. When yes, use only the last highlighted word 
            split = text.split(" ")
            if len(split) > 1:
                text = split[-1]
                print("More as one word highlighted, I will use: ", text)
                # move cursor to prevent that the wrong word(s) will be overwritten by the commit function
                cursor.setPosition(cursor.selectionEnd())
                cursor.movePosition(QTextCursor.WordLeft, QTextCursor.KeepAnchor, n = 1)
                self.textEnglish.setTextCursor(cursor)
        resultList = self.textProcessing.getMostSimilar(text)
        for index in range(len(resultList)):
            self.buttonList[index].setText(resultList[index][0])
        
    def commitText(self, text=""):
        # insert text at cursor position (if something is highlighted it will be overwritten) 
        cursor = self.textEnglish.textCursor()
        cursor.insertText(text)
   
        
class Textprocessing():
    wordVector = None
    translationTokenizer = None
    translationModel = None
    def __init__(self):
        # if a local word2vec file exist load the model, else use the gensim downloader to get a pretrained
        if os.path.isfile("models/word2vec_model"):
            self.wordVector = Word2Vec.load("models/word2vec_model").wv
        else:
            self.wordVector = gensim.downloader.load('glove-wiki-gigaword-50')
        # if the translation folder is empty load one through the transformers pipeline, else use the local model
        if len(os.listdir("models/translation")) == 0:
            self.translationTokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-en")
            self.translationModel = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-en")
        else:
            self.translationTokenizer = AutoTokenizer.from_pretrained("models/translation")
            self.translationModel = AutoModelForSeq2SeqLM.from_pretrained("models/translation")
        pass
    
    def loadModels():
        pass
    
    def getMostSimilar(self, inputText: str, n=10) -> str:
        sims = self.wordVector.most_similar(inputText.lower(), topn=n)
        return sims
    
    def getTranslation(self, inputText: str, n=10) -> str:
        encoder_input_str = inputText
        encoder_input_ids = self.translationTokenizer(encoder_input_str, return_tensors="pt").input_ids
        outputs = self.translationModel.generate(encoder_input_ids, num_beams=n, num_return_sequences=n)
        result = []
        for output in outputs:
            result.append(self.translationTokenizer.decode(output, skip_special_tokens=True))
        return result


class SettingsWindow(QtWidgets.QDialog):
    # TODO: implement
    pass

   
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    


if __name__ == '__main__':
    main()
    
