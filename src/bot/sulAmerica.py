import os
import sys
import time
import logging
import datetime
import traceback

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
from src.bot.my_logger import get_logger



class sulAmerica:
    logger = get_logger()

    def __init__(self, code, user, password, teste = True):
        
        #options = webdriver.ChromeOptions()
        
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options() 
        options.page_load_strategy = 'none'
        #options.add_argument('--log-level=4')
        
        self.driver = webdriver.Chrome(service=service, options=options)
        if not teste :
            self.driver.minimize_window()
           
        self.i = Interation(self.driver)
        
        self.driver.get("https://saude.sulamericaseguros.com.br/prestador/login/")
        
        self.login(code, user, password)
        self.start()
        
    def get(self, url):
        self.driver.get(url)    
        return True
    
    def login(self,code, user, password):
        try:
            login = Login(self.driver)
            
            #self.skip_login()
            #input('enter')
            login.set_user('//*[@id="code"]', code)
            
            login.set_user('user', user, method='id')
            
            
            login.set_password('senha', password,  method='id')
            #if self.i.locacated()
            
            self.i.click_js('//*[@id="entrarLogin"]')
            print('clickou')
            #login.click_button('/html/body/as-main-app/as-login-container/div[1]/div/as-login/div[2]/form/fieldset/button')
            
            return True

        except Exception as e:
            self.logger.error(e)
            return False
    
    def click_services(self):
        self.i.click('//*[@id="LumNav"]/li[2]/a')
        
        
    def click_faturamento(self):
        self.i.click('//*[@id="prestadorMenuSeguradoPrincipal"]/div/div/div/div/div/div[2]/a')
        
    
    def click_guia_consulta(self):
        self.i.click('/html/body/div[1]/table[10]/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div/div/div[3]/p[3]/a')
        
    
    def insert_code(self, value =  '11122222333355556666'):
        beneficiario = [0, value[:3], value[3:8], value[8:12], value[12:16], value[16:20]]
        #for i in range(1,6):
        beneficiario = value
        xpath = f'//*[@id="codigo-beneficiario-1"]'
        self.logger.info(xpath)      
        
        self.i.write(xpath, beneficiario)
        
        self.click_confirma()
            
        return True
    
    def click_confirma(self):
        self.i.click_js('//*[@id="Form_8A61F5C6407D868201407DAA886A1760"]/div/div/div/div[2]/div[3]/div[3]/button[1]')
    
    def insert_atendimento(self, value):
        xpath = '//*[@id="inclusao-consulta-pedido"]/section/div/div/section/div[2]/as-tipo-pedido-autocomplete/div/div/input'
        self.i.locacated(xpath)
        self.i.write(xpath, value)
        #
        # self.i.write_js('#inclusao-consulta-pedido > section > div > div > section > div.tipo-pedido > as-tipo-pedido-autocomplete > div > div > input', value)
        
        return True
    
    
    def click_autorization_previa(self):
        try:
            self.i.element('//*[@id="menu-usuario"]/as-item-menu[3]/li/a')
            self.get('https://credenciado.sulAmerica.com.br/pedidos-autorizacao')
            self.logger.info('clickado no auttorização previa com sucesso')
            
            return True
        except Exception as e:
            self.logger.error(e)
         
    def insert_medico(self, medico):
        self.i.write('//*[@id="nome"]', medico)
        
    def select_conselho(self, conselho = "CRM"):
        options = self.i.element('//*[@id="conselho-profissional"]', time=40)
        select = Select(options)
        select.select_by_visible_text(conselho)
        
    def select_state(self, state='PR'):
        options = self.i.element('//*[@id="uf-conselho-profissional"]', time=40)
        select = Select(options)
        select.select_by_visible_text(state)
        
    def insert_registro_conselho(self, code):
        self.i.write('//*[@id="numero-registro-conselho"]', code)
        
    def insert_cbo(self, cbo):
        path = '//*[@id="cbo"]'
        self.i.write(path, cbo)
        time.sleep(1)
        self.i.element(path).send_keys(Keys.DOWN)
        self.i.element(path).send_keys(Keys.ENTER)
        #self.i.key(path)
        #input('continuar')
        #self.i.click('//*[@id="ui-id-17"]')
        #input('continuar')
        #self.i.key('//*[@id="cbo"]')
        
    
    def select_acidente(self, value ='Não Acidente'):
        options = self.i.element('//*[@id="indicador-acidente"]', time=40)
        select = Select(options)
        select.select_by_visible_text(value)
        
    def insert_data(self):
        date = datetime.date.today().strftime('%d%m%Y')
        self.i.write('//*[@id="data-atendimento"]', date)
        return True
    
    def select_consulta(self, value= "Primeira Consulta"):
        options = self.i.element('//*[@id="tipo-consulta"]', time=40)
        select = Select(options)
        select.select_by_visible_text(value)
        
    def select_rn(self, value = 'Não'):
        options = self.i.element('//*[@id="flag-atendimento-rn"]', time=40)
        select = Select(options)
        select.select_by_visible_text(value)
        
    def select_regime_atendimento(self, value = 'Ambulatorial'):
        options = self.i.element('//*[@id="regime-atendimento"]', time=40)
        select = Select(options)
        select.select_by_visible_text(value)
        
    def insert_valor_procedimento(self, valor='11000'):
        self.i.write('//*[@id="valor-procedimento"]', valor)
        
    def click_confirma_final(self):
        self.i.click_js('//*[@id="Form_8A61F5C6407D868201407DAA95421826"]/div/div/div/div[7]/div[4]/a[1]')
    
    def get_code(self):
        el = self.i.element('//tbody/tr/td/div/b')
        return el.text

    
    def start(self):
        self.click_services()
        self.click_faturamento()
        self.click_guia_consulta()
    
    def exec_dados_atendimento(self, medico, conselho, code, cbo, uf= "PR"):
        try:
            try:
                self.insert_medico(medico)        
                self.select_conselho(conselho)
                self.select_state(uf)
                self.insert_registro_conselho(code)
                self.insert_cbo(cbo)
            except Exception as e:
                tb_info = traceback.format_exc()
                mensagem_erro = f"Ocorreu um erro: {e}\nTraceback:\n{tb_info}"
                self.logger.exception(mensagem_erro)

            try:
                self.select_acidente()
                self.insert_data()    
                self.select_consulta()
                self.select_rn()
                self.select_regime_atendimento()
                self.insert_valor_procedimento()
            except Exception as e:
                tb_info = traceback.format_exc()
                mensagem_erro = f"Ocorreu um erro: {e}\nTraceback:\n{tb_info}"
                self.logger.exception(mensagem_erro)

            self.click_confirma_final()
            code = self.get_code()
            return code
        except Exception as e:
                tb_info = traceback.format_exc()
                mensagem_erro = f"Ocorreu um erro: {e}\nTraceback:\n{tb_info}"
                self.logger.exception(mensagem_erro)
                
        
        
    
    
if __name__ == "__main__":
    sul = sulAmerica('100000009361', 'master', '837543')
    #print(1)
    #sul.login()
    #print(2)
   
   
    sul.insert_code('58201333000059520012')
 
    
    code = sul.exec_dados_atendimento('Marcos de Abreu Bonardi', 'CRM', '17741','225280',"PR")
    
    print(code)
    
    
    #input('enter')
    #print(sul.interation.verify_page('home'))
    #sul.get('https://credenciado.sul.com.br/pedidos-autorizacao')
    # sul.click_autorization_previa()
    # sul.insert_CPF('550628703')
    # sul.insert_atendimento('consulta')
    input('enter')