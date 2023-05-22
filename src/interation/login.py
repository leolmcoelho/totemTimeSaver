import os, sys

sys.path.append(os.getcwd())

from src.interation import Interation
from selenium import webdriver

from dotenv import dotenv_values


class Login:
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.interation = Interation(driver)
                
    
    def set_user(self, path, value, method = 'xpath'):
        self.interation.write(path, value, method)
        return True
    

    def set_password(self, path, value, method = 'xpath'):
        self.interation.write(path, value, method)
        return True
    

    def click_button(self, path):
        self.interation.click(path)
        return True
        
    def unimed_user(self, selector, value):
        #self.element.
        path = f'document.querySelector({selector}).value({value})'
        self.driver.execute_script()
    
if __name__ == "__main__":

    pass
    

