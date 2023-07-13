import os
import sys
import time
import pickle
import logging
import datetime
import traceback
import logging as log
sys.path.append(os.getcwd())

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from src.interation.login import Login
from src.interation import Interation
from src.bot.my_logger import get_logger
from src.interation.make_driver import Driver


os.environ['WDM_LOG'] = str(log.NOTSET)


import datetime
class Copel(Interation):
    logger = get_logger()

    def __init__(self, user, password, teste=True):

        # options = webdriver.ChromeOptions()
        self.host ='https://saude.fcopel.org.br:8443/'

        self.driver = Driver().driver
        
        if not teste:
            self.driver.minimize_window()

        super().__init__(self.driver)
        self.url = self.host + "/PlanodeSaude/"
        self.driver.get(self.url)
        
        self.login(user, password)
        

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
            #time.sleep(1)
            self.iframe('/html/body/iframe')
            self.iframe('//*[@id="principal"]')            
            
            self.access_type()
            
            login = Login(self.driver)
            login.set_user('nmUsuario', user, method='id')
            login.set_password('dsSenha', password,  method='id')
            login.click_button('btn_entrar', method='id')

            return True

        except Exception as e:
            self.logger.error(f'Erro no login: {e}')
            return False


    def access_type(self):
        self.select_option('//*[@id="tipoUsuario"]', value = 'P')    
    
    def iframe(self, seletor = '//*[@id="principal2"]'):
        iframe = self.element(seletor)
        self.driver.switch_to.frame(iframe)
    
    
    
    def autorizador(self):
        self.iframe_conteudo()
        self.iframe('/html/frameset/frame[1]')
        
        self.click_js('//*[@id="subItem_8_1"]')
        #self.driver.get(self.host + '/GuiaConsulta/ViewGuiaConsulta')
        print('click')
        
    def carteira(self, carteira):
        self.driver.switch_to.default_content()
        
        self.iframes_base()
        self.iframe_conteudo()
        self.iframe('//*[@id="paginaPrincipal"]')
                
        path = '//*[@id="CD_USUARIO_PLANO"]'
        self.write(path, carteira)
        self.key(path, 'tab')
        
        
    def crm(self, crm):
        path = '//*[@id="nr_crm"]'
        self.write(path, crm)
        self.key(path, 'tab')
        
    
    
    def salvar(self):
        self.click_js('//*[@id="btnSalvar"]')
        
        
    def requisicao(self):
        requisicao = self.get_attribute('/html/body/table[2]/tbody/tr[1]/td[1]', 'innerHTML')
        requisicao = requisicao.split(':')
        if requisicao:
            return requisicao[1]
        return False
    
    def iframes_base(self):
        self.driver.switch_to.default_content()
        self.iframe('/html/body/iframe')
        self.iframe('//*[@id="principal"]')
        
    
    def iframe_conteudo(self):
        self.iframe('/html/body/table/tbody/tr/td/iframe')

    
    def selects(self):
        infos = [
            {'value': '3', 'xpath': '//*[@id="ie_tipo_guia"]'},
            {'value': '1', 'xpath': '//*[@id="ie_tipo_consulta"]'},
            {'value': '9', 'xpath': '//*[@id="tp_acidente_consulta"]'},
            {'value': '01', 'xpath': '//*[@id="ie_regime_atendimento_consulta"]'},
        ]
        for info in infos:
            self.select_option(info['xpath'], info['value'])
        
    def btn_continuar(self):
        self.click('//*[@id="btnSalvar"]')
    
        
    
    
        
    
    
    
if __name__ == '__main__':
    USER, PASSWORD = ('56200757968', 'Procto1200@')
    os.system('cls')    
    CARTEIRA = '018164000'
    CRM = '17617'
    
    SENHA = ''
 #   Requisição:2878191	
#Nº da Guia: 2322346
    
    medico = 'Marcos de Abreu'
  
    try:
        s = Copel(USER, PASSWORD)
        s.iframes_base()
        s.autorizador()
        s.carteira(CARTEIRA)
        s.crm(CRM)
        s.selects()
        s.btn_continuar()
        re = s.requisicao()
        print(re)
        # s.verify_carteira()
        # s.medico(medico)
        # s.date()
        # s.salvar()
        # senha = s.senha()
        
        # print(senha)       
        # #s.get_cookies()
    
    except Exception as e:
            tb_info = traceback.format_exc()
            mensagem_erro = f"Ocorreu um erro: {e}\nTraceback:\n{tb_info}"
            s.logger.exception(mensagem_erro)

    
    finally:
        input('terminou')
