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


sys.path.append(os.getcwd())

from src.interation.login import Login

from src.interation import Interation


class Amil:
    
    def __init__(self, teste = True):
        
        #options = webdriver.ChromeOptions()
        
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options() 
        options.page_load_strategy = 'none'
        
        self.driver = webdriver.Chrome(service=service, options=options)
        if not teste :
            self.driver.minimize_window()
           
        self.i = Interation(self.driver)
        
        self.driver.get("https://credenciado.amil.com.br/login")
        
    def get(self, url):
        self.driver.get(url)    
        return True
    
    def login(self, user, password):
        try:
            login = Login(self.driver)
            
            #self.skip_login()
            #input('enter')
            login.set_user('//*[@id="login-usuario"]', user)
            
            
            login.set_password('//*[@id="login-senha"]', password)
            #if self.i.locacated()
            
            self.i.click_js('/html/body/as-main-app/as-login-container/div[1]/div/as-login/div[2]/form/fieldset/button')
            print('clickou')
            #login.click_button('/html/body/as-main-app/as-login-container/div[1]/div/as-login/div[2]/form/fieldset/button')
            
            return True

        except Exception as e:
            logging.error(e)
            return False
    
    def skip_login(self):
        try:
            self.i.click("finalizar-walktour",method='id', time=5)
        except:
            print('não encontrado')
            pass
        
    def insert_CPF(self, value =  '111'):
        xpath = '//*[@id="NaN"]'
        self.i.locacated(xpath)
        self.i.write_js('#NaN', value)
        self.i.click(xpath)
        self.driver.execute_script('document.querySelector("#undefined > as-input-float-label > div.input-float-label > button").disabled = false;')
        #self.driver.execute_script('document.querySelector("#undefined > as-input-float-label > div.input-float-label > button").click();')
        self.i.click('//*[@id="undefined"]/as-input-float-label/div[1]/button')
        return True
    
    
    def insert_atendimento(self, value):
        xpath = '//*[@id="inclusao-consulta-pedido"]/section/div/div/section/div[2]/as-tipo-pedido-autocomplete/div/div/input'
        self.i.locacated(xpath)
        self.i.write(xpath, value)
        #
        # self.i.write_js('#inclusao-consulta-pedido > section > div > div > section > div.tipo-pedido > as-tipo-pedido-autocomplete > div > div > input', value)
        
        return True
    
    
    def insert_data(self):
        date = datetime.date.today().strftime('%d%m%Y')
        self.i.write('//*[@id="data-pedido-medico"]', date)
        return True
        
    def verify_result(self, html):
        while "Buscando" in self.i.element(html).get_attribute('innerHTML'):
            time.sleep(0.5)
    
    
    def inserir_solicitante(self, name, CBO):
        input_name = '//*[@id="nome,-código-do-prestador,-cpf-ou-conselho"]'
        self.i.write(input_name, name)
        result = '//*[@id="results"]/li[1]'
        
        self.verify_result(result)

        self.i.element(input_name).send_keys(Keys.DOWN)
        self.i.element(input_name).send_keys(Keys.ENTER)
        
        
        ##inserir CBO
        input_CBO = '//*[@id="cbo-s"]'
        self.i.write(input_CBO, CBO)
                        
        return True
    
    def inserir_servico(self, service = "10101012"):
        self.i.write('//*[@id="inclusao-consulta-pedido"]/section/as-tipo-pedido-sadt/div[5]/as-procedimento-servico/div/ul/li[1]/as-procedimento-autocomplete/div/div/input', service)
        self.i.click_js('//*[@id="inclusao-consulta-pedido"]/section/as-tipo-pedido-sadt/div[5]/as-procedimento-servico/div/div/button')
        return True        
    
    def click_autorization_previa(self):
        try:
            self.i.element('//*[@id="menu-usuario"]/as-item-menu[3]/li/a')
            self.get('https://credenciado.amil.com.br/pedidos-autorizacao')
            time.sleep(1)
            while "pedidos-autorizacao" in self.driver.current_url:
                break
            else:
                time.sleep(0.5)  
            
            print(self.driver.current_url)
                
            logging.info('clickado no auttorização previa com sucesso')
            
            return True
        except Exception as e:
            logging.error(e)
         
    def click_incluir(self):
        self.i.click_js('//*[@id="inclusao-consulta-pedido"]/section/div[4]/button[2]')
        return True
        
    def inserir_token(self, token):
        self.i.write('//*[@id="chave"]', token)
        self.i.click_js('//*[@id="tour3-confirma"]/button')
        return True
        
        #ATENDIMENTO REALIZADO COM SUCESSO
        #//*[@id="detalhes-autorizacao"]/menu-pedido/as-message/div/p
        #DIV QUE CONTEM A MENSAGEM
        #//*[@id="detalhes-autorizacao"]/menu-pedido/as-message/div
        
    
    def verify_token(self):
        self.i.element()
        
    
    
if __name__ == "__main__":
    amil = Amil()
    print(1)
    amil.login('10604456', '@1200procto')
    print(2)
    #input('enter')
    #print(amil.interation.verify_page('home'))
    #amil.get('https://credenciado.amil.com.br/pedidos-autorizacao')
    amil.click_autorization_previa()
    amil.insert_CPF('550628703')
    amil.insert_atendimento('consulta')
    
    amil.insert_data()    
    amil.inserir_solicitante('Marcos de abreu bonardi', 225280)
    amil.inserir_servico()
    amil.click_incluir()
    
    amil.inserir_token(1111)
    input('enter')