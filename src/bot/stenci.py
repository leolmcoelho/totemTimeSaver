import logging as log
import os
import sys
import time
import json

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
from src.models.user import *
from src.bot.my_logger import get_logger

os.environ['WDM_LOG'] = str(log.NOTSET)


logging = get_logger()


class Stenci:

    def __init__(self, user, password, teste=False):

        # options = webdriver.ChromeOptions()

        service = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        #options.page_load_strategy = 'normal'
        options.add_argument('--log-level=4')
        options.add_argument(
            f'user-data-dir={os.getcwd()}/config/Profile 2')

        try:
            self.driver = webdriver.Chrome(service=service, options=options)
        except:
             self.driver = webdriver.Chrome(service=service)
        
        if not teste:
            self.driver.minimize_window()

        self.i = Interation(self.driver)

        self.driver.get("https://stenci.app")
        
        
        try:
            self.i.locacated('//*[@id="app"]/section/aside/nav/a[2]/div', 3)

        except:
            if self.logado() == False:
                self.login(user, password)
        self.click_agenda()
        
        
    def logado(self):
        try:
            if self.i.locacated('//*[@id="username"]', time=1):
                js ='document.querySelector("body > div.login-page > div.login-form > form > div.form-body > label > input[type=checkbox]").checked = true'
                self.driver.execute_script(js)
                return False
            else: 
                return True
        except:
            return False
        
    
    def login(self, user, password):
        try:
            login = Login(self.driver)

            login.set_user('//*[@id="username"]', user)

            login.set_password('//*[@id="password"]', password)

            login.click_button('/html/body/div[1]/div[3]/form/button')

            return True

        except:
            return False

    def click_agenda(self):
        self.i.click('//*[@id="app"]/section/aside/nav/a[2]')
        self.select_agenda()
        return True

    def set_client(self, client):
        self.i.write(
            '//*[@id="app"]/section/main/div/div[3]/div/div/div/div[1]/div/input',
            client)
        self.client_click()
        return True

    def client_click(self):
        self.i.click(
            '//*[@id="app"]/section/main/div/div[3]/div/table/tbody/tr/td[3]', time=40)

        # self.i.click('//*[@id="modal-appointment"]/div/div[2]/div[2]/div/ul/li[3]/a')
        return True

    def select_agenda(self):
        select_element = self.i.element('//*[@id="professional"]')
        select = Select(select_element)
        select.select_by_visible_text('[Todos]')

    def get_infos(self):
        values = {}
        paths = {
            # 'name': '//*[@id="company-name"]',
            # 'tel': '//*[@id="phone"]',

            'carteira': '//*[@id="appointment-insurance-record"]'
        }

        for path in paths.keys():
            time.sleep(1)
            el = self.i.element(paths[path]).get_attribute('value')

            values[path] = el

        select = self.i.element(
            '//*[@id="appointment-professional"]/option[2]').get_attribute('text')
        # select = Select(select)
        values['medico'] = ' '.join(select.split()[:-1])

        select_element = self.i.element('//*[@id="appointment-insurance"]')
        select = Select(select_element)
        values['convenio'] = select.all_selected_options[0].text

        logging.info(values)
        values = IStenci(**values)
        return values

    def click_registrar_atendimento(self):
        # registrar atendimento
        self.i.click_js('//*[@id="div-register-service"]/div/a/button')
        self.i.click_js('//*[@id="div-register-service"]/div/ul/li/a')

    def finalizar_amil(self, senha):
        self.click_procedimentos()
        self.click_lupa()
        self.selecionar_consulta()
        self.registra_procedimentos()
        time.sleep(2)
        self.click_sp()
        time.sleep(2)
        self.set_senha(senha)
        self.click_preencher()
        time.sleep(2)
        self.click_finalizar()
        time.sleep(1.5)
        time.sleep(2)
        self.click_salvar_espera()
        
    
    def click_salvar_espera(self):
        self.i.click_js("//button[text()='Salvar e colocar em espera']")
    
    def click_procedimentos(self):
        self.i.click('//*[@id="modal-appointment"]/div/div[2]/div[2]/div/ul/li[2]/a')
        time.sleep(1)
    
    def set_senha(self, senha):
        self.i.write('//*[@id="authorization-password"]', senha)
    
    def click_finalizar(self):
        self.i.click_js('//*[@id="modal-sadt-account"]/div/div[2]/div[3]/button[1]')
        

    def click_preencher(self):
        self.i.click('//*[@id="modal-sadt-account"]/div/div[2]/div[2]/div/div[5]/div[6]/button')
    
    def registra_procedimentos(self):
        self.i.click_js('//*[@id="div-register-service"]/div/a/button')
    
    def selecionar_consulta(self):
        xpath = "//td[text()='Consulta em Consultório']"
        self.i.click(xpath)
    
    
    def click_lupa(self):
        self.i.click('//*[@id="expenses"]/div/form/div/div/div/form/div/button')

    def click_sp(self):
        self.i.click_js("//a[text()='Guia de SP/SADT']")
        
    def click_sair(self):
        path = '//button[text()="Sair"]'
        
        
    
    
    def finalizar(self):

        self.click_procedimentos()

        self.click_lupa()
    
        self.click_registrar_atendimento()
        time.sleep(3)

        self.i.element('//*[@id="referral-service-type"]', time=30)

        self.clicks_select_final()

        el = '//*[@id="modal-appointment"]/div/div[2]/div[3]/button[3]'
        # //*[@id="modal-appointment"]/div/div[2]/div[3]/button[3]
        self.i.click_js(el, time=40)

        logging.info(self.i.element(el).get_attribute('outerHTML'))
        time.sleep(2)

    def clicks_select_final(self):
        clicks = ['//*[@id="referral-service-type"]/option[2]',
                  '//*[@id="consultation-type"]/option[2]',
                  '//*[@id="referral-type"]/option[2]'
                  ]

        for el in clicks:
            self.i.click(el,  time=40)

        el = '//*[@id="modal-particular-account"]/div/div[2]/div[3]/button[1]'
        self.i.click_js(el,  time=40)
        time.sleep(2)

    def extrair_medicos(self):
        host = 'https://stenci.app'
        self.driver.get('https://stenci.app/clinical/professionals')
        medicos = self.i.elements(
            '//*[@id="app"]/section/main/div/div[2]/div[2]/table/tbody/tr/td/a')

        all_medicos = []
        links = []
        for medico in medicos:
            links.append(medico.get_attribute('href'))

        for medico in links:
            try:
                self.driver.get(medico)

                # time.sleep(2)

                name = self.i.element(
                    '//*[@id="company-name"]').get_attribute('value')
                cpf = self.i.element(
                    '//*[@id="company-cpf"]').get_attribute('value')
                conselho = self.i.element(
                    '//*[@id="professional-council"]').get_attribute('value')
                uf = self.i.element(
                    '//*[@id="professional-council-state"]').get_attribute('value')

                especialidade = self.i.element(
                    '//*[@id="professional"]/div[5]/div[5]/table/tbody/tr[2]/td[1]').text
                name_especialidade = self.i.element(
                    '//*[@id="professional"]/div[5]/div[5]/table/tbody/tr[2]/td[2]').text

                medico_dict = {
                    'name': name,
                    'cpf': cpf,
                    'especialidade': especialidade,
                    'conselho': conselho,
                    'uf': uf,
                    'name_especialidade': name_especialidade
                }

                all_medicos.append(medico_dict)
                self.driver.get('https://stenci.app/clinical/professionals')
                time.sleep(2)

            except:
                print(medico)

        with open('medicos.json', 'w') as f:
            json.dump(all_medicos, f)


if __name__ == '__main__':

    i = time.time()

    s = Stenci("74655523549", 'crm1234', True)
    # time.sleep(20)

    # input('ta parado')
    # login = s.login()
    #time.sleep(2
               

    # s.click_agenda()
    # s.extrair_medicos()

    s.set_client('Joao Luiz Garcez Neto')
    # input('ta parado')

    # s.client_click()

    # a = s.get_infos()
    # print(a)

    s.finalizar_amil(111)

    f = time.time()

    print(f"demorou {f - i} segundos para concluir")

    input('fechou')
