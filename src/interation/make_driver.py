import os
import sys
import time
import json
import logging as log
from dotenv import dotenv_values
from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.firefox.service import Service as GeckoService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as GeckoOptions

sys.path.append(os.getcwd())
from src.bot.my_logger import get_logger
from src.models.user import *
from src.interation import Interation

os.environ['WDM_LOG'] = str(log.NOTSET)

logging = get_logger()

class Driver(Interation):

    def __init__(self, teste=False):
        
        configs = dotenv_values('config/SITE.env')
        
        if configs['DRIVER'] == 'chrome':
            logging.info('o driver é chrome')
            self.make_chrome()
                        
        elif configs['DRIVER'] == 'mozilla':
            self.make_mozilla()
            
        
        super().__init__(self.driver)

        if not teste:
            self.driver.minimize_window()
            
        
        #self.driver.get('https://timesaver.com.br/controller/read/senhas?empresa=stenci&id=1')

    def make_chrome(self):
        service = ChromeService(executable_path='config/driver/chromedriver.exe')
        options = ChromeOptions()
        options.add_argument('--log-level=4')

        try:
            self.driver = webdriver.Chrome(service=service, options=options)
        except:
            self.driver = webdriver.Chrome(service=service)

    def make_mozilla(self):
        service = GeckoService(executable_path=GeckoDriverManager().install())
        options = GeckoOptions()
        options.add_argument('--log-level=4')

        try:
            self.driver = webdriver.Firefox(service=service, options=options)
        except:
            self.driver = webdriver.Firefox(service=service)



if __name__ == '__main__':
    d = Driver()
    time.sleep(5)