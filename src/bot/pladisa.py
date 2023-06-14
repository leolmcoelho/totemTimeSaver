import os
import sys
import time
import datetime
import logging
import traceback
import logging as log

sys.path.append(os.getcwd())

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.interation import Interation
from src.interation.login import Login
from src.bot.my_logger import get_logger

os.environ['WDM_LOG'] = str(log.NOTSET)



class Pladisa(Interation):
    logger = get_logger()

    def __init__(self, user, password, teste=True):

        # options = webdriver.ChromeOptions()
        self.host ='https://pladisaonline.com.br/'

        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        # options.page_load_strategy = 'none'
        options.add_argument('--log-level=4')
        
        #options.add_argument(r'user-data-dir={}\config\Profile 2'.format(os.getcwd()))

        self.driver = webdriver.Chrome(service=service, options=options)
        
        if not teste:
            self.driver.minimize_window()

        super().__init__(self.driver)      
        self.url = self.host
        self.driver.get(self.url)
        
        self.login(user, password)

   
    def login(self, user, password):
        try:
            time.sleep(1)
            
            self.select_access()
            
            login = Login(self.driver)

            login.set_user('//div/div[2]/div/div[1]/div/input', user, method='xpath')
            login.set_password('html/body/div[17]/div/div[2]/div/div[2]/div/div[2]/div/input', password,  method='xpath')

            login.click_button('/html/body/div[17]/div/div[2]/div/div[2]/div/div[4]/div[1]/div/button', method='xpath')

            return True

        except Exception as e:
            tb_info = traceback.format_exc()
            mensagem_erro = f"Erro no login: {e}\nTraceback:\n{tb_info}"
            
            logging.error(mensagem_erro)
            return False


    def select_access(self):
        self.click_js('/html/body/div[16]/div/div/div[2]/div[7]/div[1]/div[2]/div[2]/div')    
    
    
    
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
        #self.write('//*[@id="dataAtendimento"]', date)

        #self.click('//*[@id="observacao"]')
    
    
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
        s = Pladisa('proctoclin', '0j98a1bh')
        #s.guia_page()
        #s.carteira(carteira)
        #s.verify_carteira()
        #s.medico(medico)
        #s.date()
        #s.salvar()
        #senha = s.senha()
        
        #print(senha)       
        #s.get_cookies()
    
    except Exception as e:
            tb_info = traceback.format_exc()
            mensagem_erro = f"Ocorreu um erro: {e}\nTraceback:\n{tb_info}"
            s.logger.exception(mensagem_erro)

    
    finally:
        input('terminou')
