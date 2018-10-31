import urllib.request
import posixpath
import os

video_url = ["https://dsmilab.nctu.edu.tw/static/assets/video/left_view.mp4",
             "https://dsmilab.nctu.edu.tw/static/assets/video/right_view.mp4"]


def main():
    for file in video_url:
        file_name = file.split('/')[-1]
        print('downloading: ', file_name)
        target_path = posixpath.join('data', 'map', file_name)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        urllib.request.urlretrieve(file, target_path)
    print('finish..')


if __name__ == '__main__':
    main()
