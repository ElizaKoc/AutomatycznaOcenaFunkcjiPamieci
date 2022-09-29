import csv
import pandas as pd
import win32api

from helpers.folder_generator import generate_directory


def generate_csv(recordings):
    # creating a new directory
    path = 'resources/download/'
    path_dir = generate_directory(recordings, path)

    try:
        # writing to csv file
        with open("resources/download" + str(path_dir) + "recognized_words/words.csv", "w", newline='') as outfile:
            headers = False

            for d in recordings:

                for record in recordings[str(d)].trial_list:

                    # creating a csv writer object
                    writerfile = csv.writer(outfile, delimiter=';')

                    if not headers:
                        # writing dictionary keys as headings of csv
                        #print(record)
                        writerfile.writerow(record.keys())
                        headers = True

                    # writing list of dictionary
                    #print(record.values())
                    writerfile.writerow(record.values())

        evaluation(path_dir)

    except PermissionError:
        win32api.MessageBox(0, 'File is currently in use! Close it and try again.', 'PermissionError', 0x00001000)
        generate_csv(recordings)


def evaluation(path_dir):
    path = "resources/download" + str(path_dir) + "recognized_words/words.csv"
    df = pd.read_csv(path, delimiter=';')

    col_names = [
        'trial_num',
        'recognized_words',
        'from_trial',
        'from_session',
        'off-list',
        'mem_from_trial[%]',
        #'mem_from_session[%]',
        'mem_trial_from_recog_words[%]',
        'mem_session_from_recog_words[%]'
    ]

    df_eval = pd.DataFrame(columns=col_names)

    num_words_session = 180
    num_words_trial = 12
    trial_numbers = df.trial_number.unique().tolist()

    for n in trial_numbers:
        records = df.loc[df['trial_number'] == n]
        from_session = 0
        from_trial = 0
        off_list = 0
        number_of_recognized_words = 0

        for idx, r in records.iterrows():
            if r['from_trial'] == 'yes':
                from_session = from_session + 1
                from_trial = from_trial + 1
            elif r['from_session'] == 'yes' and r['from_trial'] == 'no':
                from_session = from_session + 1
            else:
                off_list = off_list + 1

            number_of_recognized_words = number_of_recognized_words + 1

        #from_ses_perc = round(((from_session * 100) / num_words_session), 2)
        from_tri_perc = round(((from_trial * 100) / num_words_trial), 2)
        ses_from_rec_perc = round(((from_session * 100) / number_of_recognized_words), 2)
        tri_from_rec_perc = round(((from_trial * 100) / number_of_recognized_words), 2)

        new_row = {
            'trial_num': n,
            'recognized_words': [number_of_recognized_words],
            'from_trial': [from_trial],
            'from_session': [from_session],
            'off-list': [off_list],
            'mem_from_trial[%]': [from_tri_perc],
            #'mem_from_session[%]': [from_ses_perc],
            'mem_trial_from_recog_words[%]': [tri_from_rec_perc],
            'mem_session_from_recog_words[%]': [ses_from_rec_perc]
        }

        # concat row to the dataframe
        new_record = pd.DataFrame(data=new_row)
        df_eval = pd.concat([df_eval, new_record], ignore_index=True)
        #df_eval = df_eval.append(new_row, ignore_index=True)

    path = "resources/download" + str(path_dir) + "recognized_words/evaluation.csv"

    with open(str(path), "w", newline='') as empty_csv:
        csv.writer(empty_csv, delimiter=',')
        pass

    df_eval.to_csv(str(path), index=False, sep=';')
