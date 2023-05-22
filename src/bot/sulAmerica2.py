import os
import sys
import time
import logging

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


class sulAmerica:
    
    def __init__(self, teste = True):
        
        #options = webdriver.ChromeOptions()
        
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options() 
        #options.page_load_strategy = 'normal'
        
        self.driver = webdriver.Chrome(service=service, options=options)
        if not teste :
            self.driver.minimize_window()
           
        self.interation = Interation(self.driver)
        self.url = "https://sulamericahc.force.com/portalparceiros/s/login/"
        self.driver.get(self.url)
        
    def get(self, url):
        self.driver.get(url)    
        return True
    
    def login(self, user, password):
        """el = self.interation.element('//*[@id="ServiceCommunityTemplate"]/div[1]/div/div[2]/div/div/c-e-m-e-d-login-container', method='xpath')
        self.driver.switch_to.frame(el)
        print('entrou no iframe')
        """
        login = Login(self.driver)
        input('leste')
        self.interation.click('//*[@id="ServiceCommunityTemplate"]/div[1]/div/div[2]/div/div/c-e-m-e-d-login-container/div/div/div[1]/div[1]/c-e-m-e-d-login/div/span/div/div', method='xpath')
        print('clicou')
        login.set_user('//*[@id="username-1"]', user)
                    
        login.set_password('//*[@id="password-1"]', password)
        
        self.interation.click_js('//*[@id="ServiceCommunityTemplate"]/div[1]/div/div[2]/div/div/c-e-m-e-d-login-container/div/div/div[1]/div[1]/c-e-m-e-d-login/div/div[2]/button[2]')
        print('clickou')
        #login.click_button('/html/body/as-main-app/as-login-container/div[1]/div/as-login/div[2]/form/fieldset/button')
        
        return True

        
    
    def click_services(self):
        self.interation.click('//*[@id="LumNav"]/li[2]/a')
        
        
    def click_faturamento(self):
        self.interation.click('//*[@id="prestadorMenuSeguradoPrincipal"]/div/div/div/div/div/div[2]/a')
        
    
    def click_guia_consulta(self):
        self.interation.click('/html/body/div[1]/table[10]/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div/div/div[3]/p[3]/a')
        
    
    def insert_code(self, value =  '111'):
        for i in range(1,6):
            xpath = f'//*[@id="codigo-beneficiario-{i}"]'
            self.interation.write(xpath, 11)
            
            
        
        
        
        
        
        return True
    
    
    def insert_atendimento(self, value):
        xpath = '//*[@id="inclusao-consulta-pedido"]/section/div/div/section/div[2]/as-tipo-pedido-autocomplete/div/div/input'
        self.interation.locacated(xpath)
        self.interation.write(xpath, value)
        #
        # self.interation.write_js('#inclusao-consulta-pedido > section > div > div > section > div.tipo-pedido > as-tipo-pedido-autocomplete > div > div > input', value)
        
        return True
    
    
    def click_autorization_previa(self):
        try:
            self.interation.element('//*[@id="menu-usuario"]/as-item-menu[3]/li/a')
            self.get('https://credenciado.sulAmerica.com.br/pedidos-autorizacao')
            logging.info('clickado no auttorização previa com sucesso')
            
            return True
        except Exception as e:
            logging.error(e)
         
        
        
    
    
if __name__ == "__main__":
    sul = sulAmerica()
    print(1)
    sul.login('camillajeremias21@gmail.com', 'tiago123')
    #print(2)
    sul.click_services()
    sul.click_faturamento()
    sul.click_guia_consulta()
    sul.insert_code()
    
    #input('enter')
    #print(sul.interation.verify_page('home'))
    #sul.get('https://credenciado.sul.com.br/pedidos-autorizacao')
    # sul.click_autorization_previa()
    # sul.insert_CPF('550628703')
    # sul.insert_atendimento('consulta')
    input('enter')