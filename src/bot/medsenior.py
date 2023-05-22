import os
import re
import sys
import time
import getpass

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

from src.bot.my_logger import get_logger





class MedSenior(Interation):
    
    logger = get_logger()
    
    def __init__(self, user, password, teste = True):
        
        #options = webdriver.ChromeOptions()
        
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options() 
        options.page_load_strategy = 'normal'
        
        options.add_argument('--log-level=4')
        
        self.driver = webdriver.Chrome(service=service, options=options)
        if not teste :
            self.driver.minimize_window()
           
        
        super().__init__(self.driver)
        self.url = "https://ptlmedsenior2.topsaude.com.br/PortalCredenciado"
        self.driver.get(self.url)
        
        self.login(user, password)
        self.click_incluir_pedido()
        
    def get(self, url):
        self.driver.get(url)    
        return True
    
    def login(self, user, password):
        try:
            time.sleep(1)
            login = Login(self.driver)
                  
            login.set_user('usuario', user, method='id')
            
            
            login.set_password('senha', password,  method='id')
            
            login.click_button('//*[@id="login-submit"]')
            
            return True

        except Exception as e:
            self.logger.error(e)
            return False
    
    def click_services(self):
        self.click('//*[@id="LumNav"]/li[2]/a')
        
        
    def click_faturamento(self):
        self.click('//*[@id="prestadorMenuSeguradoPrincipal"]/div/div/div/div/div/div[2]/a')
        
    
    def click_guia_consulta(self):
        self.click('/html/body/div[1]/table[10]/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div/div/div[3]/p[3]/a')
        
    
    def insert_code(self, value =  '111'):
        for i in range(1,6):
            xpath = f'//*[@id="codigo-beneficiario-{i}"]'
            self.write(xpath, 11)
            
                
        return True
    
    
    def insert_atendimento(self, value):
        xpath = '//*[@id="inclusao-consulta-pedido"]/section/div/div/section/div[2]/as-tipo-pedido-autocomplete/div/div/input'
        self.locacated(xpath)
        self.write(xpath, value)
        #
        # self.write_js('#inclusao-consulta-pedido > section > div > div > section > div.tipo-pedido > as-tipo-pedido-autocomplete > div > div > input', value)
        
        return True
    
    
    def click_autorization_previa(self):
        try:
            self.element('//*[@id="menu-usuario"]/as-item-menu[3]/li/a')
            self.get('https://credenciado.MedSenior.com.br/pedidos-autorizacao')
            self.logger.info('clickado no auttorização previa com sucesso')
            
            return True
        except Exception as e:
            self.logger.error(e)
         
    def click_incluir_pedido(self):
        auth = "//a[contains(text(), 'Autorização')]"
        self.click_js(auth)
        
        pedido_path = "//a[contains(text(), 'Incluir Pedido')]"
        self.click_js(pedido_path)
        return True
    
    
    def inserir_beneficiario(self, beneficiario):
        self.entrar_iframe()
        print('entrou no primeiro')
        self.entrar_iframe()
        print('entrou no segundo')
        
        input_xpath = '//*[@id="num_associado"]'
        self.write(input_xpath, beneficiario, time=40)
        self.key(input_xpath)
        
        
        return True
    
    
    
    def inserir_cel(self, number=None):
        #ddd, cel = self.cel(21999999) 
        
        ddd_path = '//*[@id="num_ddd_cel_contato"]'
        cel_path = '//*[@id="num_cel_contato"]'
        self.write(ddd_path, '')
        self.write(cel_path, '')
        
        self.click_js('//*[@id="btnFecharContato"]')
        
        return True
    
    
    def select_tipo(self):
        select_element = self.element('//*[@id="ind_tipo_etapa"]', time=40)
        select = Select(select_element)
        select.select_by_visible_text('Solicitação de autorização pelo prestador executante')
        return True
    
    def select_consulta(self):
        self.click_js('//*[@id="ind_atendimento"]')
        time.sleep(1)
        return True

    
    def select_pedido_autorizacao(self):
        self.click_js('//*[@id="ind_tipo_emissao_guia"]')
        time.sleep(1)
        return True
    
    def entrar_iframe(self, seletor = '//*[@id="principal2"]'):
        iframe = self.element(seletor)
        self.driver.switch_to.frame(iframe)
    
    def click_finalizar(self):
        self.driver.switch_to.default_content()
        
        self.entrar_iframe()
        
        
        iframe = self.element('//*[@id="toolbarMvcToAsp"]')
        self.driver.switch_to.frame(iframe)
        
        self.click_js('//*[@id="btn_acao_incluir"]')
        
        self.driver.switch_to.default_content()
        
        self.entrar_iframe()
        self.entrar_iframe()       
        
        self.click_js('//*[@id="ind_tipo_emissao_guia"]')
        self.click_js('//*[@id="btnInclusaoViaPrestadorOK"]')
        return True

    
    def get_code(self):
        self.driver.switch_to.default_content()
        self.entrar_iframe()
        self.entrar_iframe()    
        #self.click('//*[@id="divPrincipal"]/div[1]')
        status = self.get_attribute('//*[@id="nom_situacao"]')
        self.logger.info(status)
        
        if status != 'Autorizado':
            return False
        senha = self.get_attribute('//*[@id="tbTodosProcedimentos"]/tbody/tr[2]/td[5]', 'innerHTML')
        senha = re.sub(r'\D', '', senha)
        return senha            
        

    def final(self):
        self.select_tipo()
        self.select_consulta()       
        self.select_pedido_autorizacao()
        self.click_finalizar()
        
        return self.get_code()
    
        
    

if __name__ == "__main__":
    try:
        med = MedSenior('0001852', 'P03340')
        input('enter')
        #med.inserir_beneficiario('0645451')
        
        #med.inserir_cel('21974082703')
        senha = '10000953358'
        pedido = '1985223'
        code = med.get_code()
        print(code)
    finally:
        
        input('enter')
    #print(med.interation.verify_page('home'))
    #med.get('https://ptlmedsenior2.topsaude.com.br/PortalCredenciado/HomePortalCredenciado/Home/AreaLogada#PORCRED9_00')
    # med.click_autorization_previa()
    # med.insert_CPF('550628703')
    # med.insert_atendimento('consulta')
    #input('enter')