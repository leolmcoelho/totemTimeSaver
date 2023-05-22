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


class Amil:
    
    def __init__(self, user, password, teste = True):
        
        #options = webdriver.ChromeOptions()
        
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options() 
        #options.page_load_strategy = 'normal'
        options.add_argument('--log-level=4')
        self.driver = webdriver.Chrome(service=service, options=options)
        if not teste :
            self.driver.minimize_window()
           
        self.i = Interation(self.driver)
        
        self.driver.get("https://credenciado.amil.com.br/login")
        
        self.login(user, password)
        
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
        self.i.write(xpath, value)
        self.i.click(xpath)
        self.driver.execute_script('document.querySelector("#undefined > as-input-float-label > div.input-float-label > button").disabled = false;')
        #self.driver.execute_script('document.querySelector("#undefined > as-input-float-label > div.input-float-label > button").click();')
        self.i.click('//*[@id="undefined"]/as-input-float-label/div[1]/button')
        return True
    
    
    def set_atendimento(self, value):
        xpath = '//*[@id="inclusao-consulta-pedido"]/section/div/div/section/div[2]/as-tipo-pedido-autocomplete/div/div/input'
        #//*[@id="inclusao-consulta-pedido"]/section/div/div/section/div[2]/as-tipo-pedido-autocomplete/div/div/input
        xpath2 = '//*[@id="results"]/li[2]'
        #self.i.locacated(xpath)
        
        js = 'document.querySelector("#results").classList.toggle("resultListShow")'
        
        self.i.click_js(xpath)
        self.i.write(xpath, value)
        
        el = self.i.get_attribute(xpath)
        
        print(el)
        
        #self.i.locacated('//*[@id="results"]', 40)
        #print('ffoi')
        #self.driver.execute_script(js)
        #self.i.click_js(xpath2)
        #
        # self.i.write_js('#inclusao-consulta-pedido > section > div > div > section > div.tipo-pedido > as-tipo-pedido-autocomplete > div > div > input', value)
        
        return True
    
    
    
    def insert_atendimento(self, value):
        self.set_atendimento(value)
        xpath = '//*[@id="inclusao-consulta-pedido"]/section/div/div/section/div[2]/as-tipo-pedido-autocomplete/div/div/input'
                
        for _ in range(5):
            el = self.i.get_attribute(xpath)
            if el == value:
                
                self.i.element(xpath).clear()
                self.set_atendimento(value)
                time.sleep(3)
            else:
                break
            
        print(el)
        
    
    def insert_data(self):
        date = datetime.date.today().strftime('%d%m%Y')
        self.i.write('//*[@id="data-pedido-medico"]', date)
        return True
        
    def verify_result(self, html):
        while "Buscando" in self.i.element(html).get_attribute('innerHTML'):
            time.sleep(0.5)
    
    
    def set_solicitante(self, name):
        input_name = '//*[@id="nome,-código-do-prestador,-cpf-ou-conselho"]'
        self.i.write(input_name, name)
        result = '//*[@id="results"]/li[1]'
        
        time.sleep(1)
        self.verify_result(result)
        

        self.i.element(input_name).send_keys(Keys.DOWN)
        self.i.element(input_name).send_keys(Keys.ENTER)
        
        
        ##inserir CBO
        time.sleep(2)
        
        return True
    
    def set_CBO(self, CBO):
        
        input_CBO = '//*[@id="cbo-s"]'
        
        self.i.write(input_CBO, CBO)
        try:
            self.verify_result('//*[@id="results"]/li', time=3)
        except:
            logging.error('erro no buscando')
        #self.i.element(input_name).send_keys(Keys.DOWN)
        self.i.element(input_CBO).send_keys(Keys.ENTER)
        
        time.sleep(2)
                        
        
    
    def inserir_solicitante(self, name, CBO):
        self.set_solicitante(name)
        self.set_CBO(CBO)
        
        input_name = '//*[@id="nome,-código-do-prestador,-cpf-ou-conselho"]'
        #xpath = '//*[@id="inclusao-consulta-pedido"]/section/div/div/section/div[2]/as-tipo-pedido-autocomplete/div/div/input'
                
        for _ in range(5):
            el = self.i.get_attribute(input_name)
            if el == name:
                
                self.i.element(input_name).clear()
                self.set_solicitante(name)
                time.sleep(1.5)
            else:
                print(el)
                break
        
        input_CBO = '//*[@id="cbo-s"]'
        for _ in range(5):
            
            el = self.i.get_attribute(input_CBO)
            if el == CBO:
                
                self.i.element(input_CBO).clear()
                self.set_CBO(CBO)
                time.sleep(1.5)
            else:
                print(el)
                break
            
        
            
        print(el)
    
    
    def inserir_servico(self, service = "10101012"):
        self.i.write('//*[@id="inclusao-consulta-pedido"]/section/as-tipo-pedido-sadt/div[5]/as-procedimento-servico/div/ul/li[1]/as-procedimento-autocomplete/div/div/input', service)
        self.i.click_js('//*[@id="inclusao-consulta-pedido"]/section/as-tipo-pedido-sadt/div[5]/as-procedimento-servico/div/div/button')
        return True        
    
    def click_autorization_previa1(self):
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
            
    def click_autorization_previa(self):
        try:
            self.i.element('//*[@id="menu-usuario"]/as-item-menu[3]/li/a')
            #self.get('https://credenciado.amil.com.br/pedidos-autorizacao')
            time.sleep(1)
            self.i.click_js('//*[@id="menu-usuario"]/as-item-menu[3]/li/a')  
            
            print(self.driver.current_url)
                
            logging.info('clickado no auttorização previa com sucesso')
            
            return True
        except Exception as e:
            logging.error(e)
    
             
    def click_incluir(self):
        self.i.click_js('//*[@id="inclusao-consulta-pedido"]/section/div[4]/button[2]')
        return True
        
    def inserir_token(self, token):
        self.i.write('//*[@id="chave"]', token, time=40)
        self.i.click_js('//*[@id="tour3-confirma"]/button')
        logging.info("click no butao do token")
        return True
        
    
    def verify_token(self):
        response = self.i.element('//*[@id="detalhes-autorizacao"]/menu-pedido/as-message/div/p').text
        
        if response == 'TOKEN inválido':
            return False
        
        else:
            return True
    
    
    def get_senha(self):
        path = '//*[@id="detalhes-autorizacao"]/menu-pedido/div[1]/ul/li[6]'
        html = self.i.element(path, time=30).text.split('\n')
        if len(html) > 2:
            return html[1]
        
        return False


    def verificar_load_page(self):
        for _ in range(3):
            if not self.driver.current_url == 'https://credenciado.amil.com.br/pedidos-autorizacao':
                self.driver.refresh()
                self.click_autorization_previa()
                time.sleep(2)
            else:
                
                print(f'parou na vez {_}')
                break    
        
      
        
          
    
    
if __name__ == "__main__":
    amil = Amil('10604456', '@1200procto')
    print(1)
    #amil.login()
    print(2)
 
    

    amil.click_autorization_previa()
    amil.verificar_load_page()
    amil.insert_CPF('059416270')
    amil.insert_atendimento('consulta')


    amil.insert_data()
    # input('esperar')
    amil.inserir_solicitante('Marcos de abreu bonardi', 225280)
    amil.inserir_servico()
    amil.click_incluir()

    #status(400)

    #token = get_token()
    for _ in range(3):
        senha = amil.get_senha()
        if senha:
            break
        
    #zerar_token()
    amil.inserir_token('123456')
    
    
    if amil.verify_token():
        senha = False
    logging.info('erro no token')
    
    input('sair')

 