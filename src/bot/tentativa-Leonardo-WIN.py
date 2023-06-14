import os
import sys
import time

sys.path.append(os.getcwd())

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


from webdriver_manager.chrome import ChromeDriverManager

import logging as log
sys.path.append(os.getcwd())
os.environ['WDM_LOG'] = str(log.NOTSET)
from src.interation import Interation
from src.interation.login import Login

class Video(Interation):
    #herança
    def __init__(self) -> None:
        self.host ='https://www.youtube.com/watch?v=L_VC8GKuUps&ab_channel=Felca'
        
        options = Options()
        service = Service(executable_path=ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service=service, options=options)

        super().__init__(self.driver)
        #fazer para a herança
        self.driver.get(self.host)

    def start_video(self):
        print('iniciou o video')
        self.click('//*[@id="movie_player"]/div[29]/div[2]/div[1]/button', time=30)
    
    def option(self):
        print('abriu configurações')
        self.click('//*[@id="movie_player"]/div[29]/div[2]/div[2]/button[3]', time=30)

    
    def velocity(self):
        print('mudando velocidade')
        self.click('//*[@id="ytp-id-18"]/div/div/div[2]/div[2]', time=5)
        
        time.sleep(2)

        self.click('//*[@id="ytp-id-18"]/div/div/div[2]/div[3]')
    
    def titulo(self):
            #"pega o conteudo de dentro do html, o texto, por exemplo"
            titulo = self.get_attribute('//*[@id="title"]/h1/yt-formatted-string', 'innerHTML')
            return titulo
        
if __name__ == '__main__':

    video = Video()
    video.start_video()
    video.option()
    video.velocity()
    video.titulo()

    input("Aperte enter para fechar o terminal")
