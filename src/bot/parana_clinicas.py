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


class ParanaClinicas(Interation):
    
    def __init__(self,user, password, teste = True):
        
        #options = webdriver.ChromeOptions()
        
        service = Service(executable_path=ChromeDriverManager().install())
        options = Options() 
        #options.page_load_strategy = 'none'
        options.add_argument('--log-level=4')
        
        self.driver = webdriver.Chrome(service=service, options=options)
        if not teste :
            self.driver.minimize_window()
           
        super().__init__(self.driver)
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
             
            login.set_user('/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[8]/td/table/tbody/tr[1]/td[2]/input', user)
            
            
            login.set_password('senha', password,  method='id')
            #if self.locacated()
            
            #self.click_js('//*[@id="login-submit"]')
            
            login.click_button('//*[@id="btn_enviar"]')
            
            return True

        except Exception as e:
            logging.error(f'Erro no login: {e}')
            return False
    
    def click_services(self):
        print('iniciou o click')
        #input('inicar sistema')
        el = self.element('topFrame', method='id')
        self.driver.switch_to.frame(el)
        logging.info('entrou no frame TopFrame')
    
        self.click('/html/body/div[1]', method='xpath')
        #print('achou o elemento')
        self.driver.switch_to.default_content()
        
        
    def entrar_frame_content(self):
        el = self.element('frameConteudo', method='id')
        self.driver.switch_to.frame(el)
        return True
           
    
    def click_guia_consulta(self):
        self.entrar_frame_content()
        
        self.click('//*[@id="5485"]/div[1]/span')
        self.click('//*[@id="5486"]/span/a')
        
    
    def insert_code(self, value =  '111'):
    
        xpath = f'//*[@id="tissBeneficiarioVO.numCarteira"]'
        self.write(xpath, value)
        
        return True
    
    
    def insert_atendimento(self, value):
        xpath = '//*[@id="inclusao-consulta-pedido"]/section/div/div/section/div[2]/as-tipo-pedido-autocomplete/div/div/input'
        self.locacated(xpath)
        self.write(xpath, value)
        #
        # self.write_js('#inclusao-consulta-pedido > section > div > div > section > div.tipo-pedido > as-tipo-pedido-autocomplete > div > div > input', value)
        
        return True
    
    def item_15(self, doctor):
        

        #click 3 pontos
        self.click('//*[@id="divGuiaSolicitacao"]/div[1]/table[10]/tbody/tr[2]/td[1]/input[5]')
        
        frame =self.element('//*[@id="popupFrame"]')
        self.driver.switch_to.frame(frame)
        
        path_input ='/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[2]/tbody/tr/td[2]/input'
        self.write(path_input, doctor)
        self.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[3]/tbody/tr/td/input')
        self.select_medico()
        
        self.driver.switch_to.default_content()
        self.entrar_frame_content()
        
    def item_19(self, value = '225280'):
        
        
        self.click('//*[@id="divGuiaSolicitacao"]/div[1]/table[10]/tbody/tr[2]/td[5]/input[3]')
        
        el = self.element('popupFrame', method='id')
        self.driver.switch_to.frame(el)
        
        self.write('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[2]/tbody/tr/td[2]/input', value)
        self.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[3]/tbody/tr/td/input')
        self.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[5]/tbody/tr[2]/td[1]/input')
        
        self.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/div/input[2]')
        
        self.driver.switch_to.default_content()
        self.entrar_frame_content()
        
        
    def select_medico(self):
        self.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/table[5]/tbody/tr[3]/td[1]/input')
        self.click('/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/form/div/input[2]')
        
    def item_25(self, procedimento:str = '10101012', descricao:str = 'Consulta em consultorio', quantidade=1):
        self.driver.switch_to.default_content()
        self.entrar_frame_content()
        self.write('//*[@id="tissItemProcediSolicitadoVO.codItem"]', procedimento)
        #input('enter')
        self.write('//*[@id="tissItemProcediSolicitadoVO.desItem"]', descricao)
        self.write('//*[@id="tissItemProcediSolicitadoVO.quantidadeSolicitada"]', quantidade)
        #time.sleep(3)
        self.click('//*[@id="imgSalvarProcedimentoSolicitado"]')
        #input('Enter')
        print('fez a inserção')
        
    def click_autorization_previa(self):
        try:
            self.element('//*[@id="menu-usuario"]/as-item-menu[3]/li/a')
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
            #self.click(xpath_menu)
            
            pass
        except:
            #input('deu erro')
            pass
        
        el = self.element('//*[@id="main-menu"]')
        els = el.find_elements('xpath', '//li')
        for el in els:
            if 'Autorização' in el.get_attribute('outerHTML'):
                el.click()
                #print(el.get_attribute('outerHTML'))
                
        
        js = 'document.querySelector("#sm-16811458605225508-1").mouseover()'
        
        self.driver.execute_script(js)
        
        # self.click_js(xpath_menu)
        # print('clicou')
        
        xpath = '//*[@id="sm-16811448388603662-2"]/li[1]/a'
        self.click(xpath)
        
    def item_31(self, CNES):
        self.write('//*[@id="tissGuiaSolicitacaoSpSadtVO.tissContratadoExecutanteVO.numCnes"]', CNES)
        
        
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
            
            self.element(path).clear()
            self.write(path, value)
            
    def click_confirma(self):
        self.click_js('//*[@id="btConfirmar"]')
        
    def get_senha(self):
        senha = self.element('//tbody/tr[3]/td[2]/b/font').text
        return senha
        
    
    def exec(self, carteira, medico, CNES = '5171288'):
        self.insert_code(carteira)
        self.item_13()
        self.item_15(medico)
        self.item_19()
        self.item_25()
        self.item_31(CNES)
        time.sleep(1.5)
        self.click_confirma()
        
        return self.get_senha()
        
        
if __name__ == "__main__":
    
    a = ParanaClinicas('1253_atend', 'saudi@pr')
   
 
    
    senha = a.exec('1037356', 'Marcos de Abreu Bonardi', )
    print(senha)
    
    #input('enter')
    #print(sul.interation.verify_page('home'))
    #sul.get('https://ptlmedsenior2.topsaude.com.br/PortalCredenciado/HomePortalCredenciado/Home/AreaLogada#PORCRED9_00')
    # sul.click_autorization_previa()'
    # sul.insert_CPF('550628703')
    # sul.insert_atendimento('consulta')
    senha =' 26580923'
    input('INPUT final')