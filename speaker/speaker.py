# Чтение вслух
from pygame import mixer
import time
from gtts import gTTS
from PyQt5 import QtCore


class Speaker(QtCore.QThread):

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent=parent)

    def run(self):
        self.sound_file = './speaker/speech.mp3'
        with open('./speaker/speech.txt', 'r') as text:
            self.phrase = text.read()
        # Инициализируем звуковое устройство
        mixer.init()
        # Эта строка отправляет предложение которое нужно озвучить гуглу
        tts = gTTS(text=self.phrase, lang='ru')
        # Получаем от гугла озвученное предложение в виде mp3 файла
        # Проигрываем полученный mp3 файл
        tts.save(self.sound_file)
        mixer.music.load(self.sound_file)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        # закрываем звуковое устройство
        mixer.stop
        mixer.quit

# say_it("Эта штука говорящая! Слушай!")