import os
import sys
import time
import logging

from selenium import webdriver

import datetime

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

from  src.interation.login import Login

from src.interation import Interation


class sulAmerica(Interation):
    
    def __init__(self, teste = True):
        
        #options = webdriver.ChromeOptions()
        
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options() 
        #options.page_load_strategy = 'normal'
        
        self.driver = webdriver.Chrome(service=service, options=options)
        
        super().__init__(self.driver)

        if not teste :
            self.driver.minimize_window()

        self = Interation(self.driver)
        self.url = "https://sulamericahc.force.com/portalparceiros/s/login/"
        self.driver.get(self.url)
        
    def get(self, url):
        self.driver.get(url)    
        return True
    
    def login(self, user, password):
        """el = self.element('//*[@id="ServiceCommunityTemplate"]/div[1]/div/div[2]/div/div/c-e-m-e-d-login-container', method='xpath')
        self.driver.switch_to.frame(el)
        print('entrou no iframe')
        """
        login = Login(self.driver)
        #input('teste')
        self.click('//*[@id="ServiceCommunityTemplate"]/div[1]/div/div[2]/div/div/c-e-m-e-d-login-container/div/div/div[1]/div[1]/c-e-m-e-d-login/div/span/div/div', method='xpath')
        print('clicou')
        login.set_user('//*[@id="username-1"]', user)
                    
        login.set_password('//*[@id="password-1"]', password)
        
        self.click_js('//*[@id="ServiceCommunityTemplate"]/div[1]/div/div[2]/div/div/c-e-m-e-d-login-container/div/div/div[1]/div[1]/c-e-m-e-d-login/div/div[2]/button[2]')
        #print('clickou')
        #login.click_button('/html/body/as-main-app/as-login-container/div[1]/div/as-login/div[2]/form/fieldset/button')
        
        return True

    def click_nova_consulta(self):
        self.click('//*[@id="ServiceCommunityTemplate"]/div[3]/div/div[2]/div[2]/div/div[1]/button')
        #print('foi')
    

    def insert_carteira(self, value):
        xpath = '//*[@id="input-17"]'
        #self.locacated(xpath)0
        self.write(xpath, value)
        #print('completou')
        #time.sleep(30)
        
    
    def click_buscar(self):
        self.click('//*[@id="ServiceCommunityTemplate"]/div[3]/div/div[2]/div/div[1]/article/div[2]/div[2]/p[3]/button')
        #print('proximo')

    def click_confirmar_usar(self):
        self.click('//*[@id="ServiceCommunityTemplate"]/div[3]/div/div[2]/div/div[1]/article/div[2]/div[2]/div[1]/div/div/button[1]')

    def select_medico(self, medico):
        self.select_option('//select', text = medico, time=30)


    def insert_date(self):
        date = datetime.date.today().strftime('%d/%m/%Y')
        self.write('//*[@id="input-30"]"]', date)

        date_atual = datetime.now().strftime('%H:%M')  # Obter a data e hora atual no formato "dd/mm/aaaa HH:MM"
        self.write('//*[@id="combobox-input-34"]', date_atual) 


    def click_presencial(self):
        self.click('//*[@id="tipoConsulta"]/lightning-radio-group/fieldset/div/span[1]/label/span[2]')
    
    
    def click_concluir(self):
        self.click('//*[@id="ServiceCommunityTemplate"]/div[3]/div/div[2]/div/div[1]/article/div[2]/div[2]/div[4]/button[2]')
    
    
    
   
        
        
    
    
if __name__ == "__main__":

    MEDICO= 'MARCOS DE ABREU BONARDI'
    CARTEIRA  = '79758000003940011'

    sul = sulAmerica()
    print(1)
    sul.login('camillajeremias21@gmail.com', 'tiago123')
    #print(2)
    sul.click_nova_consulta()
    sul.insert_carteira(CARTEIRA)
    sul.click_buscar()
    sul.click_confirmar_usar()
    #input('Esperar')
    try:
        sul.select_medico(MEDICO)

    except:
        input("\n\n\nEsperar")

    #sul.insert_date()
    sul.click_presencial()

    
    input('enter')