import requests
import os


def toVoice(text):
    # get sound from baidu
    user_agent = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT6.1;Trident / 5.0)"}
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
            print(item + ' to voice done -> ' + item + '.mp3')
            text.remove(item)
        else:
            os.remove(item + '.mp3')
    return text


if __name__ == '__main__':
    source = open('vocal.txt', 'r')
    lines = source.readlines()
    words = []
    for word in lines:
        word = word.replace('\n', '')
        words.append(word)
    print(str(len(words)) + ' words detected')

    while len(words) > 0:
        words = toVoice(words)

    fileList = os.listdir()
    mp3List = []
    for file in fileList:
        if file.find('.mp3') != -1:
            mp3List.append(file)
    print(str(len(mp3List)) + ' mp3 detected')
    file = open('mp3List.txt', 'a')
    absolutePath = os.path.abspath(os.curdir)
    for mp3 in mp3List:
        with open('blank/blank.mp3', 'rb') as source:
            data = source.read()
        source.close()
        with open(mp3.split('.')[0] + '_blank.mp3', 'ab') as target:
            target.write(data)
        target.close()
        line = ' \'' + absolutePath + '/' + mp3 + '\'' + '\n'
        line2 = ' \'' + absolutePath + '/' + mp3.split('.')[0] + '_blank.mp3' + '\'' + '\n'
        print(line2)
        file.write('file' + line)
        file.write('file' + line2)
    file.close()
    command = 'ffmpeg -f concat -safe 0 -i ' + absolutePath + '/' + 'mp3List.txt -c copy output.mp3'
    os.system(command)

    # Delete waste
    os.remove('mp3List.txt')
    fileList = os.listdir()
    for file in fileList:
        if file.find('.mp3') != -1 and file.find('output') == -1:
            os.remove(file)
    print('Done')
