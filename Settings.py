from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QTextCursor, QColor
import sys
import yaml


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(SettingsWindow, self).__init__()
        # load GUI
        uic.loadUi("Schreibhilfe_Settings_GUI.ui", self)
        self.buttonConfirm.clicked.connect(self.confirm)
        # preload fields if possible
        config = self.load_config()
        if config != None:
            self.word_vector_path.setText(config[0]['Settings']['word_vector_path'])
            self.translation_model_path.setText(config[0]['Settings']['translation_model_path'])
            self.generation_model_path.setText(config[0]['Settings']['generation_model_path'])
            if config[0]['Settings']['keep_original_translation']:
                self.keep_original_translation_text_true.setChecked(True)
            elif config[0]['Settings']['keep_original_translation'] == False:
                self.keep_original_translation_text_false.setChecked(True)
            if config[0]['Settings']['load_model_if_needed']:
                self.load_model_if_needed_true.setChecked(True)
            elif config[0]['Settings']['load_model_if_needed'] == False:
                self.load_model_if_needed_false.setChecked(True)
        pass


    def confirm(self):
        # read settings from fields 
        word_vector = self.word_vector_path.text()
        if word_vector == "":
            word_vector = "default"
        translation_model = self.translation_model_path.text()
        if translation_model == "":
            translation_model = "default"
        generation_model = self.generation_model_path.text()
        if generation_model == "":
            generation_model = "default"
        keep_original = False
        if self.keep_original_translation_text_true.isChecked():
            keep_original = True
        elif self.keep_original_translation_text_false.isChecked():
            keep_original = False
        load_model_if_needed = False
        if self.load_model_if_needed_true.isChecked():
            load_model_if_needed = True
        elif self.load_model_if_needed_false.isChecked():
            load_model_if_needed = False

        # TODO: check if models can be loaded

        # save into yaml file
        config = [
            {
                'Settings': {
                    'word_vector_path': word_vector,
                    'translation_model_path': translation_model,
                    'generation_model_path': generation_model,
                    'keep_original_translation': keep_original,
                    'load_model_if_needed': load_model_if_needed,
                }
            }
        ]
        with open("config.yaml", 'w') as configfile:
            data = yaml.dump(config, configfile)
            print("Setting successful saved")

        # close window
        print("Changes to the models are only applied after a restart")
        self.close()


    def load_config(self):
        try:
            with open("config.yaml", "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print("No config file exist yet")
        except:
            print("Couldn't read the config file")
        return None
