import os
import sys
import time
import logging
import datetime

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import logging as log

os.environ['WDM_LOG'] = str(log.NOTSET)


sys.path.append(os.getcwd())

from src.interation.login import Login

from src.interation import Interation

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

class Imprimir(Interation):
    
    def __init__(self,teste = True):
        
        
        #options = webdriver.ChromeOptions()

        if True:
            service = Service(executable_path=ChromeDriverManager().install())
            options = Options() 
            options.page_load_strategy = 'normal'
            options.add_argument('--log-level=4')
            options.add_argument(f"--kiosk-printing"  )

            self.driver = webdriver.Chrome(service=service, options=options)
        
        #service=FirefoxService(GeckoDriverManager().install())
        path = os.getcwd() + '/geckodriver.exe'
        #
        
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options() 
        options.page_load_strategy = 'normal'
        options.add_argument('--log-level=4')
        self.driver = webdriver.Chrome(service=service, options=options)

        if not teste :
            self.driver.minimize_window()
           
        #self.i = Interation(self.driver)
        super().__init__(self.driver)
        print('carregou a pagina')
        self.driver.get("http://localhost:5000/teste")

        print('carregou a pagina')
        
    
   
        
    def mudar_janela(self):
        # Mude o foco para a janela de impressão
        print('print das janelas')
        self.driver.window_handles[-1]
        self.driver.switch_to.window(self.driver.window_handles[-1])

        print('print das janelas')
        print(self.driver.window_handles)
        self.driver.switch_to.window(self.driver.window_handles[0])

    def run(self):
        

        builder = ActionChains(self.driver)
        imprimir = self.click('//*[@id="imprimir"]')
        #btn = self.i.element('//*[@id="sidebar"]//print-preview-button-strip//div/cr-button[1]')
        #builder.move_to_element(btn).click()
        
        builder.key_down(Keys.ENTER)
        
        builder.perform()

        
if __name__ == '__main__':
    i = Imprimir()
    i.run()
    #i.click()
    #rint('print')
    #i.mudar_janela()
    input('enter')
    