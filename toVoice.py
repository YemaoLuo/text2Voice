import os

import requests


def toVoice(text):
    # get sound from baidu
    user_agent = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT6.1;Trident / 5.0)"}
    count = 1
    for item in text:
        url = 'https://fanyi.baidu.com/gettts?lan=en&text=' + item + '&spd=3&source=web'
        resp = requests.get(url, headers=user_agent)
        resp.close()
        content = resp.content
        with open(item + '.mp3', 'wb') as i:
            i.write(content)
        i.close()
        stats = os.stat(item + '.mp3')
        if stats.st_size != 0:
            print(str(count) + '/' + str(len(text) + count) + ':' + item + ' to voice done -> ' + item + '.mp3 ')
            count += 1
            text.remove(item)
        else:
            os.remove(item + '.mp3')
    return text


def main():
    input('All files except provided should be removed in this dir. '
          'Words should be stored in vocal.txt, ffmpeg should be pre installed. Press enter to continue.')
    source = open('./vocal.txt', 'r')
    lines = source.readlines()
    words = []
    for word in lines:
        word = word.replace('\n', '')
        words.append(word)
    print(str(len(words)) + ' words detected.')

    maxCount = len(words) * 100
    count = 0
    words_copy = []
    for word in words:
        words_copy.append(word)
    while len(words) > 0:
        if count > maxCount:
            print('Transform words to voice error. Over max retry times.')
            return
        words = toVoice(words)
        count += 1

    fileList = os.listdir()
    mp3List = []
    for word in words_copy:
        for file in fileList:
            if file.find('.mp3') != -1 and file.find(word) != -1:
                mp3List.append(file)
                break
    print(str(len(mp3List)) + ' mp3 detected')
    file = open('./mp3List.txt', 'a')
    absolutePath = os.path.abspath(os.curdir)
    for mp3 in mp3List:
        with open('./blank/blank.mp3', 'rb') as source:
            data = source.read()
        source.close()
        with open(mp3.split('.')[0] + '_blank.mp3', 'ab') as target:
            target.write(data)
        target.close()
        line = ' \'' + absolutePath + '/' + mp3 + '\'' + '\n'
        line2 = ' \'' + absolutePath + '/' + mp3.split('.')[0] + '_blank.mp3' + '\'' + '\n'
        file.write('file' + line)
        file.write('file' + line2)
    file.close()
    command = 'ffmpeg -f concat -safe 0 -i ' + absolutePath + '/' + 'mp3List.txt -c copy output.mp3'
    os.system(command)

    # Delete waste
    os.remove('./mp3List.txt')
    fileList = os.listdir()
    for file in fileList:
        if file.find('.mp3') != -1 and file.find('output') == -1:
            os.remove(file)
    print('Done')


if __name__ == '__main__':
    main()
