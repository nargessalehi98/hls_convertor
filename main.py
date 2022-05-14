import os
import csv
import requests
import ffmpeg_streaming
from ffmpeg_streaming import Formats


def save_hls_format(path_to_file):
    """
    Convert and save the mp4 file in the input address to the hls format
    :param path_to_file:
    :return:
    """
    try:
        video = ffmpeg_streaming.input(path_to_file, f='mp4')
        dash = video.dash(Formats.h264())
        dash.auto_generate_representations()
        path_to_save = path_to_file + "_hls/"
        os.makedirs(path_to_save, exist_ok=True)
        dash.output(path_to_save)
    except Exception as err:
        print(err)


def downloader(url, path_to_save, file_name):
    """
    download mp4 file in give url and save in given address with given name
    :param url:
    :param path_to_save:
    :param file_name:
    :return:
    """
    try:
        downloaded_file = requests.get(url)
        path_to_save = path_to_save + "/" + file_name
        with open(path_to_save, 'wb') as file:
            file.write(downloaded_file.content)
        save_hls_format(path_to_save)
    except Exception as err:
        print(err)


def excel_reader(file_name, path_to_save):
    """
    read data in give mp4 file name and pass data to downloader
    :param file_name:
    :param path_to_save:
    :return:
    """
    try:
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            try:
                for row in csv_reader:
                    downloader(row[1], path_to_save, row[0])
            except Exception as e:
                print(str(e))
    except Exception as err:
        print(err)


if __name__ == "__main__":
    try:
        print("Enter csv file_name (placed in root of project) and path_to_save in Two separate lines:")
        file_name = input()
        path_to_save = input()
        excel_reader(file_name, path_to_save)
    except Exception as err:
        print(err)
