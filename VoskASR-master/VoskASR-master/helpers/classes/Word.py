class Word:
    """ A class representing a word from the JSON format for vosk speech recognition API """

    def __init__(self, word_dict):
        """
        Parameters:
          word_dict (dict) dictionary from JSON, containing:
            conf (float): degree of confidence, from 0 to 1
            end (float): end time of the pronouncing the word, in seconds
            start (float): start time of the pronouncing the word, in seconds
            word (str): recognized word
        """
        self.word = word_dict["word"]
        self.conf = word_dict["conf"]
        self.start = word_dict["start"]
        self.end = word_dict["end"]

        self.word_dict = {"word": word_dict["word"], "conf": word_dict["conf"], "start": word_dict["start"],
                          "end": word_dict["end"]}

    def to_string(self):
        """ Returns a string describing this instance """
        if len(self.word) >= 3:
            return "{:20} from {:.2f} sec to {:.2f} sec, confidence is {:.2f}%".format(
                self.word, self.start, self.end, self.conf * 100)

    def check_for_all_previous_trials(self, recording_words):
        self.word_dict['from_session'] = 'no'
        for trial_number in recording_words:
            trial = recording_words[trial_number]
            for recording_word in trial:
                if str.lower(recording_word) == self.word:
                    self.word_dict['from_session'] = 'yes'
                    break

    def check_for_this_trial(self, recording_words):
        trial_number = list(recording_words.keys())[-1]
        trial = recording_words[trial_number]
        self.word_dict['from_trial'] = 'no'
        for recording_word in trial:
            if str.lower(recording_word) == self.word:
                self.word_dict['from_trial'] = 'yes'
                continue
            self.word_dict['trial_number'] = trial_number

    def to_dict(self, recording_words):
        if len(self.word) >= 3:
            self.check_for_all_previous_trials(recording_words)
            self.check_for_this_trial(recording_words)
            return self.word_dict
