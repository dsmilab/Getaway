import urllib.request

video_url = ["https://dsmilab.nctu.edu.tw/static/assets/video/left_view.mp4",
                    "https://dsmilab.nctu.edu.tw/static/assets/video/right_view.mp4"]

if __name__ == '__main__':
    for file in video_url:
        file_name = file.split('/')[-1]
        print('downloading: ', file.split('/')[-1])
        urllib.request.urlretrieve (file, file_name)
    print('finish..')
