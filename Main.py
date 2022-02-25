import sys
import os
import gensim.downloader
from gensim.models import Word2Vec
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QTextCursor, QColor
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM
import language_tool_python


class MainWindow(QtWidgets.QDialog):
    textProcessing = None
    buttonList = []
    languageTool = language_tool_python.LanguageTool('en-US')
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        # GUI stuff
        uic.loadUi("Schreibhilfe_MainWindow.ui", self)
        self.buttonSynonyms.clicked.connect(self.findSynonyms)
        self.buttonTranslation.clicked.connect(self.translate) 
        self.buttonSettings.clicked.connect(self.openSettings)
        self.buttonSuggestWord.clicked.connect(self.suggestNextWord)
        self.buttonGenerateText.clicked.connect(self.generateText)
        self.buttonSpellCheck.clicked.connect(self.spellcheck)
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
            
    def suggestNextWord(self):
        suggestedWords = self.textProcessing.generateText(self.textEnglish.toPlainText(), 1)
        for index, word in enumerate(suggestedWords):
            self.buttonList[index].setText(word)
        pass
    
    def generateText(self):
        generatedText = self.textProcessing.generateText(self.textEnglish.toPlainText(), 50)
        self.textGerman.setText(generatedText[0])
        pass
    
    def spellcheck(self):
        # remove all red color from former spellchecks
        blackColor = QColor(0, 0, 0)
        text = self.textEnglish.toPlainText()
        self.textEnglish.setTextColor(blackColor)
        self.textEnglish.setText(text)
        # check for spelling error and save them in 'matches'
        matches = self.languageTool.check(self.textEnglish.toPlainText())
        redColor = QColor(255, 0, 0)
        cursor = self.textEnglish.textCursor()
        # iterate through all matches and set color from text in question to red
        for match in matches:
            cursor.setPosition(match.offset, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, match.errorLength)
            text = cursor.selectedText()
            self.textEnglish.setTextCursor(cursor)
            self.textEnglish.setTextColor(redColor)
            cursor.insertText(text)
        # TODO: show suggestions for found spell errors
        pass
                    
    def commitText(self, text=""):
        # insert text at cursor position (if something is highlighted it will be overwritten) 
        blackColor = QColor(0, 0, 0)
        self.textEnglish.setTextColor(blackColor)
        cursor = self.textEnglish.textCursor()        
        cursor.insertText(text)
        
    def openSettings(self):
        # TODO
        print("Not implemented yet!")
        pass
   
        
class Textprocessing():
    wordVector = None
    translationTokenizer = None
    translationModel = None
    generationModel = None
    generationTokenizer = None
    def __init__(self):
        # if a local word2vec file exist load the model, else use the gensim downloader to get a pretrained
        if os.path.isfile("models/word2vec_model"):
            self.wordVector = Word2Vec.load("models/word2vec_model").wv
            print("loaded custom word2vec model")
        else:
            self.wordVector = gensim.downloader.load('glove-wiki-gigaword-50')
            print("loaded glove-wiki-gigaword")
        # if the translation folder is empty load one through the transformers pipeline, else use the local model
        if len(os.listdir("models/translation")) == 0:
            self.translationTokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-en")
            self.translationModel = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-en")
            print("loaded default translation model")
        else:
            self.translationTokenizer = AutoTokenizer.from_pretrained("models/translation")
            self.translationModel = AutoModelForSeq2SeqLM.from_pretrained("models/translation")
            print("loaded custom translation model")
        # use default gpt2-small model, if there is no other text generation model 
        if len(os.listdir("models/textgeneration")) == 0:
            self.generationTokenizer = AutoTokenizer.from_pretrained("gpt2")
            self.generationModel = AutoModelForCausalLM.from_pretrained("gpt2")
            print("loaded gpt2")
        else:            
            self.generationTokenizer = AutoTokenizer.from_pretrained("models/textgeneration")
            self.generationModel = AutoModelForCausalLM.from_pretrained("models/textgeneration")
            print("loaded custom causal language model")
        # TODO: exception handling? Who needs exception handling?!
    
    def loadModels():
        pass
    
    def getMostSimilar(self, inputText: str, n=10) -> str:
        sims = self.wordVector.most_similar(inputText.lower(), topn=n)
        return sims
    
    def getTranslation(self, inputText: str, n=10):
        encoder_input_str = inputText
        encoder_input_ids = self.translationTokenizer(encoder_input_str, return_tensors="pt").input_ids
        outputs = self.translationModel.generate(encoder_input_ids, num_beams=n, num_return_sequences=n)
        result = []
        for output in outputs:
            result.append(self.translationTokenizer.decode(output, skip_special_tokens=True))
        return result
    
    def generateText(self, inputText: str, length: int):
        inputs = self.generationTokenizer(inputText, return_tensors="pt")
        input_ids = inputs["input_ids"]
        if length == 1:
            outputs = self.generationModel.generate(
                input_ids, 
                max_new_tokens=1,
                num_beams=10, 
                num_return_sequences=10,
                max_length = 500
            )
        else:
            outputs = self.generationModel.generate(
                input_ids, 
                do_sample=True, 
                max_length=length, 
                top_k=50, 
                temperature=0.8, 
                num_beams=5, 
                num_return_sequences=1,
                early_stopping=True
            )
        result = []
        for output in outputs:
            text = self.generationTokenizer.decode(output, skip_special_tokens=True)
            # TODO: find a smoother solution to remove the inputText
            result.append(text.replace(inputText, ""))
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
    
