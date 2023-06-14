
import logging as log
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
import sys
import time

sys.path.append(os.getcwd())
from src.interation.login import Login
from src.interation import Interation

sys.path.append(os.getcwd())
os.environ['WDM_LOG'] = str(log.NOTSET)


class Video(Interation):
    # herança
    def __init__(self) -> None:
        self.host = 'https://www.youtube.com/watch?v=L_VC8GKuUps&ab_channel=Felca'

        options = Options()
        service = Service(executable_path=ChromeDriverManager().install())

        self.driver = webdriver.Chrome(service=service, options=options)

        super().__init__(self.driver)
        # fazer para a herança
        self.driver.get(self.host)

    def start_video(self):
        print('iniciou o video')
        self.click('//*[@id="movie_player"]/div[29]/div[2]/div[1]/button', time=30)

    def option(self):
        print('abriu configurações')
        self.click('//*[@id="movie_player"]/div[29]/div[2]/div[2]/button[3]', time=30)

    def velocity(self):
        print('mudando velocidade')
        self.click('//*[@id="ytp-id-18"]/div/div/div[1]', time=5)

        # self.click('//*[@id="ytp-id-18"]/div/div/div[2]/div[3]')

    def legend(self):
        print('ativando legenda')
        self.click('//*[@id="movie_player"]/div[29]/div[2]/div[2]/button[2]', time=5)

    def titulo(self):
        # "pega o conteudo de dentro do html, o texto, por exemplo"
        titulo = self.get_attribute('//*[@id="title"]/h1/yt-formatted-string', 'innerHTML')
        # return titulo
        print(titulo)

    def get_all_videos(self):

        self.driver.get('https://www.youtube.com/@RadioBandNewsFM/videos')
        els = self.elements(
            "//a[contains(@class, 'yt-simple-endpoint') and starts-with(@href, '/watch?v=')]")

        for el in els:
            print(el.get_attribute('href'))
            print('\n')


if __name__ == '__main__':

    video = Video()
    video.get_all_videos()
    # video.start_video()
    # video.option()
    # video.velocity()
    # video.titulo()
    # video.legend()
    # video.option()

    input("Aperte enter para fechar o terminal")
