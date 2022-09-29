import os
import shutil


def generate_directory(recordings, path):
    if recordings['1']:
        filepath = recordings['1'].filepath
        name = filepath.split('\\')
        name = ((name[0]).split('/'))[-1]

        path = str(path) + str(name)

        # check whether the specified path exists or not
        is_exist = os.path.exists(path)

        if not is_exist:
            # create a new directory because it does not exist
            os.makedirs(path)
            print("The new directory is created!")

            generate_subdirectory(str(path) + '/recognized_words')
            #generate_subdirectory(str(path) + '/charts')

        return "/" + str(name) + "/"
    return '/'


def generate_subdirectory(path):
    # check whether the specified path exists or not
    is_exist = os.path.exists(path)

    if not is_exist:
        # create a new directory because it does not exist
        os.makedirs(path)


def clear_directory(folder):
    folder = folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
