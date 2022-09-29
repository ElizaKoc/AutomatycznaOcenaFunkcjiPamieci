import csv
import pandas as pd
import os

import win32api
from kivy.app import App

from helpers.classes.Recording import Recording


class Data:
    def __init__(self, dir_path, file_path, **kwargs):
        super().__init__(**kwargs)

        self.dir_path = dir_path
        self.file_path = file_path
        self.all_words = set()
        self.recording_words = {}
        self.recordings = {}

        self.load_words()
        self.load_audio()
        self.speech_to_text()

    def load_words(self):

        """
        with open(self.file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            next(csv_reader)
            for row in csv_reader:
                recording_number = row[0]
                word = row[1]
                self.all_words.add(word)
                self.recording_words.setdefault(recording_number, []).append(word)
            # print('rec_wor', self.recording_words)
            # print('all', self.all_words)
        """
        #it should be imported from 'table.csv' file for each session
        csv_reader = (pd.read_csv(self.file_path))[['LIST', 'WORD']]
        for idx, row in csv_reader.iterrows():
            recording_number = row['LIST']
            word = row['WORD']
            self.all_words.add(word)
            self.recording_words.setdefault(recording_number, []).append(word)

    def load_audio(self):
        for filename in os.listdir(self.dir_path):
            f = os.path.join(self.dir_path, filename)
            # checking if it is a file
            if os.path.isfile(f):
                if f.endswith('.wav'):
                    self.process_audio_file(f)
                else:
                    win32api.MessageBox(0, 'Incorrect audio data format!', 'Error', 0x00001000)
                    App.get_running_app().restart()

    def process_audio_file(self, filepath):
        # prepare data for asr model
        recording_num = os.path.basename(filepath)
        recording_num = recording_num.split('_')[1]
        recording_num = recording_num.split('.')[0]
        recording_num = recording_num.lstrip("0")
        recording_words_subset = {key: value for key, value in self.recording_words.items()
                                  if int(key) <= int(recording_num)}
        recording_object = Recording(filepath=filepath, recording_words=recording_words_subset)
        self.recordings[recording_num] = recording_object

    def speech_to_text(self):
        session_list = []
        for recording in self.recordings:
            self.recordings[recording].label_words()
            print(self.recordings[recording].trial_list)
