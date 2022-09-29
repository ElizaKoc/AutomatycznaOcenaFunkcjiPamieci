from helpers.folder_generator import generate_directory


def generate_chart(recordings):
    # creating a new directory
    path = 'resources/download/'
    path_dir = generate_directory(recordings, path)