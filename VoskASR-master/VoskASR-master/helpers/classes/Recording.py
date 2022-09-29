from vosk import Model, KaldiRecognizer
import helpers.classes.Word as custom_word
import wave
import json

from helpers.preprocessing import preprocess


class Recording:
    def __init__(self, filepath, recording_words, **kwargs):
        super().__init__(**kwargs)

        self.trial_list = None
        self.filepath = filepath
        self.recording_words = recording_words

        # print(self.filepath)
        # print(self.recording_words)

    def kaldi(self):
        #model = Model(lang="en-us")
        #model = Model(model_name='vosk-model-en-us-0.21')
        #model = Model(model_name='vosk-model-small-en-us-0.15')
		
		"""
		the selected model should be downloaded 
		from https://alphacephei.com/vosk/models
		and the path to it should be provided, 
		such as "recources/model/name_of_selected_model"
		"""
		model = Model("path_to_model") 
		
        path_out = preprocess(self.filepath)
        wf = wave.open(path_out, 'rb')
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        results = []

        while True:
            data = wf.readframes(16000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part_result = json.loads(rec.Result())
                results.append(part_result)

        # convert list of JSON dictionaries to list of 'Word' objects
        list_of_words = []
        for sentence in results:
            if len(sentence) == 1:
                # sometimes there are bugs in recognition
                # and it returns an empty dictionary
                # {'text': ''}
                continue
            for obj in sentence['result']:
                w = custom_word.Word(obj)  # create custom object
                list_of_words.append(w)  # and add it to list

        wf.close()  # close audiofile

        # print(rec.FinalResult())
        return list_of_words

    def label_words(self):
        list_of_words = self.kaldi()
        trial_list = []

        for word in list_of_words:
            # print(word.to_string())
            if len(word.word) >= 3:
                word_dict = word.to_dict(self.recording_words)
                trial_list.append(word_dict)
        self.trial_list = trial_list
