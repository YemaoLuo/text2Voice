import os

import requests
from pydub import AudioSegment


def toVoice(text):
    # get sound from baidu
    user_agent = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT6.1;Trident / 5.0)"}
    count = len(text)
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
            print(str(count) + ' remain : ' + item + ' to voice done -> ' + item + '.mp3 ')
            count -= 1
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
    print(str(len(words) + 1) + ' words detected.')

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

    track = AudioSegment.from_mp3(mp3List[0])
    track += AudioSegment.from_mp3(mp3List[0]) - 10000
    track += AudioSegment.from_mp3(mp3List[0]) - 10000
    for i in range(1, len(mp3List)):
        print(str(i) + '/' + str(len(mp3List)) + ' concat in progress')
        mp3 = mp3List[i]
        track += AudioSegment.from_mp3(mp3)
        track += AudioSegment.from_mp3(mp3) - 10000
        track += AudioSegment.from_mp3(mp3) - 10000

    track.export('output.mp3', format='mp3')
    # Delete waste
    fileList = os.listdir()
    for file in fileList:
        if file.find('.mp3') != -1 and file.find('output') == -1:
            os.remove(file)
    print('Done')


if __name__ == '__main__':
    main()
