import os


def download(path: str):
    video_path = r'D:\video'
    try:
        os.system('you-get -o %s %s' % (video_path, path))
    except Exception as err:
        print("发生异常!", err)


if __name__ == '__main__':
    download('https://www.bilibili.com/video/BV1Nf4y1a7hp?from=search&seid=17620702911965010499')
