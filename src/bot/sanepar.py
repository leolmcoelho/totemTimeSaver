import os
import sys
import time
import logging
sys.path.append(os.getcwd())

import datetime

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys

import traceback
import pickle

import logging as log

from src.interation.login import Login
from src.interation import Interation
from src.bot.my_logger import get_logger

os.environ['WDM_LOG'] = str(log.NOTSET)



class Sanepar(Interation):
    logger = get_logger()

    def __init__(self, user, password, teste=True):

        # options = webdriver.ChromeOptions()
        self.host ='https://novowebplansanepar.facilinformatica.com.br/GuiasTISS'

        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        # options.page_load_strategy = 'none'
        options.add_argument('--log-level=4')
        
        #options.add_argument(r'user-data-dir={}\config\Profile 2'.format(os.getcwd()))

        self.driver = webdriver.Chrome(service=service, options=options)
        
        if not teste:
            self.driver.minimize_window()

        super().__init__(self.driver)
        self.url = self.host + "/Logon"
        self.driver.get(self.url)
        #self.set_cookies()
        self.login(user, password)
        # self.click_services()
        # self.click_guia_consulta()

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        # Salve os cookies em um arquivo
        cookies_path = os.path.join(os.getcwd(), 'config', 'cookies.pkl')

        with open(cookies_path, 'wb') as file:
            pickle.dump(cookies, file)
            
    def set_cookies(self):
        cookies_path = os.path.join(os.getcwd(), 'config', 'cookies.pkl')
        with open(cookies_path, 'rb') as file:
            cookies = pickle.load(file)
        
        # Adicione os cookies ao novo driver
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    
    
    def login(self, user, password):
        try:
            time.sleep(1)
            
            self.access_type()
            
            login = Login(self.driver)

            login.set_user('login-entry', user, method='id')

            login.set_password('password-entry', password,  method='id')

            login.click_button('BtnEntrar', method='id')

            return True

        except Exception as e:
            logging.error(f'Erro no login: {e}')
            return False


    def access_type(self):
        self.select_option('//*[@id="tipoAcesso"]', value = '22')    
    
    
    
    def guia_page(self):
        self.element('//*[@id="menuPrincipal"]/div/div[2]/a')
        self.driver.get(self.host + '/GuiaConsulta/ViewGuiaConsulta')
        print('click')
        
    def carteira(self, carteira):
        self.write('//*[@id="beneficiario"]', carteira)
        
    def verify_carteira(self):
        self.click('//*[@id="executante"]')
        for _ in range(5):
            carteira = self.get_attribute('//*[@id="nomeBeneficiario"]')
            print(carteira)
            time.sleep(0.7)
            if carteira:
                return carteira
        
        return False
    
    
    def medico(self, medico):
        path = '//*[@id="executante"]'
        self.write(path, medico)
        time.sleep(1)
        self.key(path, 'down')
        self.key(path, 'enter')
        
        self.click('//*[@id="div-especialidadesMedicas"]/a[1]')
        
        
    def date(self):
        date = datetime.date.today().strftime('%d/%m/%Y')
        self.write('//*[@id="dataAtendimento"]', date)

        self.click('//*[@id="observacao"]')
    
    
    def salvar(self):
        self.click_js('//*[@id="guiaconsulta"]/div[1]/div/div[1]/div[2]/button[1]')
        self.click_js('//*[@id="button-0"]')
        
    def senha(self):
        senha = self.get_attribute('//*[@id="dialogText"]/div[4]/span', 'innerHTML')
        #senha = senha.split('</b>')
        return senha
    
if __name__ == '__main__':
    # user, senha = ()
    #print(os.getcwd())
    os.system('cls')
    
    carteira = '37910701'
    medico = 'Marcos de Abreu'
  
    try:
        s = Sanepar('03340883000177', 'Procto1200@')
        s.guia_page()
        s.carteira(carteira)
        s.verify_carteira()
        s.medico(medico)
        s.date()
        s.salvar()
        senha = s.senha()
        
        print(senha)       
        #s.get_cookies()
    
    except Exception as e:
            tb_info = traceback.format_exc()
            mensagem_erro = f"Ocorreu um erro: {e}\nTraceback:\n{tb_info}"
            s.logger.exception(mensagem_erro)

    
    #finally:
        #input('terminou')
