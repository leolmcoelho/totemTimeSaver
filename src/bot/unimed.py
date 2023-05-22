import os
import sys
import time



from selenium import webdriver

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.chrome.service import Service as CService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.edge.service import Service as IEService
from webdriver_manager.microsoft  import IEDriverManager
from selenium.webdriver.support.select import Select



#from selenium.webdriver.ie.options import EI_Options



from selenium.webdriver.chrome.options import Options as C_Options

sys.path.append(os.getcwd())

from src.interation.login import Login

from src.interation import Interation
from src.bot.my_logger import get_logger

import logging as log

os.environ['WDM_LOG'] = str(log.NOTSET)



class Unimed:
    logger = get_logger()
    
    
    def __init__(self,user, password, navegador = 'chrome', teste = None) -> None:
        
       
        if navegador == 'chrome':
            options = C_Options()
            
            #path = f"user-data-dir={os.getcwd()}\webdependencies\Profile 5"
            ##print(path)
            #options.add_argument(path)
            service = CService(executable_path=ChromeDriverManager().install())
            #service = ChromeDriverManager().install()
            self.driver = webdriver.Chrome(service=service, options=options)
        
        elif navegador == 'mozila':
            #self.driver = webdriver.Firefox(service=service, options=options)
            #service=FirefoxService(GeckoDriverManager().install())
            #service=(GeckoDriverManager().install())
            ##print(os.getcwd() + '/geckodriver.exe')
            #service = FirefoxService(executable_path = os.getcwd() + '\geckodriver.exe')
            path = os.getcwd() + '/geckodriver.exe'
            #path = GeckoDriverManager().install()
            self.driver = webdriver.Firefox(executable_path=path)        
        
        elif navegador == 'edge':
            #options = EI_Options()
            #options.page_load_strategy = 'none'
            service = 'IEDriverServer.exe'
            #service = (IEDriverManager().install())
            self.driver = webdriver.Ie(executable_path=service)            
        
        
        self.interation = Interation(self.driver)
        self.host = 'chrome-extension://moffahdcgnjnglbepimcggkjacdmpojc/ieability.html?url=https://autorizador.unimedcuritiba.com.br/'
        self.host = 'https://autorizador.unimedcuritiba.com.br/'
        
        #self.host = "chrome-extension://moffahdcgnjnglbepimcggkjacdmpojc/options.html"
        if not teste :
            self.driver.minimize_window()
        self.driver.get(self.host)
        
        #print(2)
        
        self.login(user, password)
        self.page_exec()
        
    def login(self, user:str, password:str):
        
        user_path = "ctl00_conteudo_TxbLogin"
        pass_path = '//*[@id="ctl00_conteudo_TxbSenha"]'
        button_path = '//*[@id="ctl00_conteudo_BtnConectar"]'
        
        login = Login(self.driver)
        #self.driver.execute_script('document.querySelector("#ctl00_conteudo_BtnConectar").click()')
        login.set_user(user_path, user,method='id')
        
        login.set_password(pass_path, password)
        
        login.click_button(button_path)
        
        #self.driver.execute('document.querySelector("#ctl00_conteudo_BtnConectar").click()')
        
        return True
    
        
    def page_exec(self):
        route = 'AutenticarBeneficiarioExecConsulta.aspx'
        path  = self.host + route
        
        #self.interation.click(path)
        #print('vai dar reload')
        self.verify_page('PaginaInicial.aspx')
        self.driver.get(path)
        self.verify_page(route)
        #print('deu')
        
    def set_beneficiary(self, number:str):
        #//*[@id="ctl00_ctl00_conteudo_txbBenef1"]
        #//*[@id="ctl00_ctl00_conteudo_txbBenef2"]
        #//*[@id="ctl00_ctl00_conteudo_txbBenef3"]
        numbers = {
            1: number[0:4],
            2: number[4:16],
            3: number[16:17]
        }
        
        for i in range(1,4):
            
            selector = f'ctl00_ctl00_conteudo_txbBenef{i}'
            #print(i)
            self.interation.click(selector, method='id')
            
            #self.interation.write(selector, numbers[i], method='id')
            try:
                self.interation.key(selector, 'home', method='id')
            except Exception as e:
                self.logger.error(e)
                #print(e)
            self.interation.write(selector, numbers[i], method='id')
        
            time.sleep(1)
            
            self.click_send()
            
    
    def click_send(self):
        self.interation.click('//*[@id="ctl00_ctl00_conteudo_btnEnviar"]')
    
           
    def verify_page(self, param, time_break = 10):
        initial = time.time()
        
        while time.time() - initial < time_break:
            url = self.driver.current_url
        
            url =  url.split('/')
            if param in url:
                return True
        
        return False
    
    def get_value(self):
        el = self.interation.element('//*[@id="ctl00_ctl00_conteudo_ddlExecutante"]').get_attribute('value')
        return el
    
    
    def set_value(self, value):
        self.driver.get('https://autorizador.unimedcuritiba.com.br/DigitarConsulta32.aspx')
        selector = "ctl00_conteudo_txtNumeroGuiaPrestador"
        #self.interation.click(selector, method='id')
                
                #self.interation.write(selector, numbers[i], method='id')
        ##print('vai dar key')
        self.interation.key(selector, 'home', method='id')
        #print('vai escrever')
        self.interation.write(selector, value, method='id')
        
    def click_final(self):
        s = '//*[@id="ctl00_conteudo_ddlTipoConsulta"]/option[2]'
        self.interation.click(s)
        
        selector = '//*[@id="ctl00_conteudo_btnExecutar"]'
        self.interation.click(selector)
        
    
    def verify_conclusion(self):
        try:
            xpath = '//*[@id="ctl00_conteudo_rptResultadoGuia_ctl01_lblRecibo"]/b'
        
            el = self.interation.element(xpath, time=15).text
        
        
            if el == "VERDE":
                return True
                        
        except Exception as e:
            self.logger.exception(e)
        
        return False
        
    
        
    def select(self, medico='Marcos de Abreu Bonardi'):
        medico = medico.upper()
        options = 'ctl00_ctl00_conteudo_ddlExecutante'
        options = self.interation.element(options, method='id', time=40)
        select = Select(options)
        
        select.select_by_visible_text(medico)
        ##print(select.options)
        
        pass
        
        
if __name__ == '__main__':
    
            
    carteira = '00320000069749256'
    medico = 'DILERMANDO PEREIRA DE ALMEIDA NETO'
    def unimed(carteira, medico):
        for _ in range(3):
            try:
                print(f'carteira {carteira}')
                u = Unimed(teste = True)
                #('terminou de carregar') 
                senhas = {'user':'con2546', 'password':'procto1200'}
                u.login(senhas['user'], senhas['password'])
                #('fechar')
                u.page_exec()
                #('fechar')
                #print(u.driver.current_url)
                u.select(medico)

                u.set_beneficiary(carteira)
                u.click_send()
                #('aperte enter')
                try:
                    u.driver.get('https://autorizador.unimedcuritiba.com.br/DigitarConsulta32.aspx')
                    u.set_value(medico)
                except Exception as e:
                    print(e)
                u.click_final()
                
                concluido = u.verify_conclusion()
                print(concluido)
                input('CLique para sair')
                break
                
            except Exception as e:
                self.logger.exception(e)
                continue
    unimed(carteira, medico)
        
        
        #https://autorizador.unimedcuritiba.com.br/DigitarConsulta32.aspx
        #https://autorizador.unimedcuritiba.com.br/MostrarResultadoGuia.aspx