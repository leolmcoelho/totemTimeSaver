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
from selenium.webdriver.support import expected_conditions as EC 

from selenium.webdriver.common.print_page_options import PrintOptions
from selenium.webdriver.common.alert import Alert

import logging as log

os.environ['WDM_LOG'] = str(log.NOTSET)
  

sys.path.append(os.getcwd())

from src.interation.login import Login

from src.interation import Interation


class ParanaClinicas:
    
    def __init__(self,user, password, teste = True):
        
        #options = webdriver.ChromeOptions()
        
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options() 
        #options.page_load_strategy = 'none'
        options.add_argument('--log-level=4')
        
        self.driver = webdriver.Chrome(service=service, options=options)
        if not teste :
            self.driver.minimize_window()
           
        self.i = Interation(self.driver)
        self.url = "https://paranaclinicas.saudi.com.br/saudi/welcome.do?task=abreLogin"
        self.driver.get(self.url)
        
        self.login(user, password)
        self.click_services()
        self.click_guia_consulta()
        
    def get(self, url):
        self.driver.get(url)    
        return True
    
    def login(self, user, password):
        try:
            time.sleep(1)
            login = Login(self.driver)
            
            #self.skip_login()
            #input('enter')
            
            
            login.set_user('/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[8]/td/table/tbody/tr[1]/td[2]/input', user)
            
            
            login.set_password('senha', password,  method='id')
            #if self.i.locacated()
            
            #self.i.click_js('//*[@id="login-submit"]')
            
            login.click_button('//*[@id="btn_enviar"]')
            
            return True

        except Exception as e:
            logging.error(f'Erro no login: {e}')
            return False
    
    def click_services(self):
        print('iniciou o click')
        #input('inicar sistema')
        el = self.i.element('topFrame', method='id')
        self.driver.switch_to.frame(el)
        logging.info('entrou no frame TopFrame')
    
        self.i.click('/html/body/div[1]', method='xpath')
        #print('achou o elemento')
        self.driver.switch_to.default_content()
        
        
    def entrar_frame_content(self):
        el = self.i.element('frameConteudo', method='id')
        self.driver.switch_to.frame(el)
        return True
           
    
    def click_guia_consulta(self):
        self.entrar_frame_content()
        
        self.i.click('//*[@id="5485"]/div[1]/span')
        self.i.click('//*[@id="5486"]/span/a')
        
    
    def insert_code(self, value =  '111'):
    
        xpath = f'//*[@id="tissBeneficiarioVO.numCarteira"]'
        self.i.write(xpath, value)
        
        return True
    
    
    def insert_atendimento(self, value):
        xpath = '//*[@id="inclusao-consulta-pedido"]/section/div/div/section/div[2]/as-tipo-pedido-autocomplete/div/div/input'
        self.i.locacated(xpath)
        self.i.write(xpath, value)
        #
        # self.i.write_js('#inclusao-consulta-pedido > section > div > div > section > div.tipo-pedido > as-tipo-pedido-autocomplete > div > div > input', value)
        
        return True
    
    def item_15(self, doctor):
        

        #click 3 pontos
        self.i.click('//*[@id="divGuiaSolicitacao"]/div[1]/table[10]/tbody/tr[2]/td[1]/input[5]')
        
        frame =self.i.element('//*[@id="popupFrame"]')
        self.driver.switch_to.frame(frame)
        
        path_input ='/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[2]/tbody/tr/td[2]/input'
        self.i.write(path_input, doctor)
        self.i.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[3]/tbody/tr/td/input')
        self.select_medico()
        
        self.driver.switch_to.default_content()
        self.entrar_frame_content()
        
    def item_19(self, value = '225280'):
        
        
        self.i.click('//*[@id="divGuiaSolicitacao"]/div[1]/table[10]/tbody/tr[2]/td[5]/input[3]')
        
        el = self.i.element('popupFrame', method='id')
        self.driver.switch_to.frame(el)
        
        self.i.write('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[2]/tbody/tr/td[2]/input', value)
        self.i.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[3]/tbody/tr/td/input')
        self.i.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[5]/tbody/tr[2]/td[1]/input')
        
        self.i.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/div/input[2]')
        
        self.driver.switch_to.default_content()
        self.entrar_frame_content()
        
        
    def select_medico(self):
        self.i.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[5]/tbody/tr[3]/td[1]/input')
        self.i.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/div/input[2]')
        
    def item_25(self, procedimento:str = '10101012', descricao:str = 'Consulta em consultorio', quantidade=1):
        self.driver.switch_to.default_content()
        self.entrar_frame_content()
        self.i.write('//*[@id="tissItemProcediSolicitadoVO.codItem"]', procedimento)
        self.i.write('//*[@id="tissItemProcediSolicitadoVO.desItem"]', descricao)
        self.i.write('//*[@id="tissItemProcediSolicitadoVO.quantidadeSolicitada"]', quantidade)
        self.i.click('//*[@id="imgSalvarProcedimentoSolicitado"]')
        input('Enter')
        print('vez a inserção')
        
    def click_autorization_previa(self):
        try:
            self.i.element('//*[@id="menu-usuario"]/as-item-menu[3]/li/a')
            self.get('https://credenciado.MedSenior.com.br/pedidos-autorizacao')
            logging.info('clickado no auttorização previa com sucesso')
            
            return True
        except Exception as e:
            logging.error(e)
         
    
    def click_incluir_pedido(self):
        print('vai clicar')
       
        
        xpath_menu = '//*[@id="sm-16811463678817988-1"]'
        #16811458605225508
        # id="sm-16811470290144385-1"
        try:
            #self.i.click(xpath_menu)
            
            pass
        except:
            #input('deu erro')
            pass
        
        el = self.i.element('//*[@id="main-menu"]')
        els = el.find_elements('xpath', '//li')
        for el in els:
            if 'Autorização' in el.get_attribute('outerHTML'):
                el.click()
                #print(el.get_attribute('outerHTML'))
                
        
        js = 'document.querySelector("#sm-16811458605225508-1").mouseover()'
        
        self.driver.execute_script(js)
        
        # self.i.click_js(xpath_menu)
        # print('clicou')
        
        xpath = '//*[@id="sm-16811448388603662-2"]/li[1]/a'
        self.i.click(xpath)
        
    def item_31(self, CNES):
        self.i.write('//*[@id="tissGuiaSolicitacaoSpSadtVO.tissContratadoExecutanteVO.numCnes"]', CNES)
        
        
    def test_print(self):
        #self.driver.execute_script('window.print()')
        import base64
        from io import BytesIO
        import PyPDF2
        print_options = PrintOptions()
        print_options.page_ranges = ['1']
        #print_options.orientation = 'LANDSCAPE'
        base64code = self.driver.print_page(print_options)
        pdf_data = base64.b64decode(base64code)
        pdf_file = BytesIO(pdf_data)
        with open('print.pdf', 'wb') as f:
            f.write(pdf_file.getbuffer())
        
        return True
    
    def item_13(self, value = 1253):
        paths = ['//*[@id="tissGuiaSolicitacaoSpSadtVO.tissContratadoExecutanteVO.codPrestador"]',
                 '//*[@id="tissGuiaSolicitacaoSpSadtVO.tissContratadoSolicitanteVO.codPrestador"]']
       
        for path in paths:
            
            self.i.element(path).clear()
            self.i.write(path, value)
    
    def exec(self, carteira, medico, CNES ):
        self.insert_code(carteira)
        self.item_13()
        self.item_15(medico)
        self.item_19()
        self.item_25()
        self.item_31(CNES)
        
        
if __name__ == "__main__":
    
    a = ParanaClinicas('12553_atend', 'saudi@p')
   
 
    
    
    
    #input('enter')
    #print(sul.interation.verify_page('home'))
    #sul.get('https://ptlmedsenior2.topsaude.com.br/PortalCredenciado/HomePortalCredenciado/Home/AreaLogada#PORCRED9_00')
    # sul.click_autorization_previa()
    # sul.insert_CPF('550628703')
    # sul.insert_atendimento('consulta')
    input('enter')