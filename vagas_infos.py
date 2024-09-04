import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from time import sleep


chrome_options = Options()
chrome_options.add_experimental_option("detach", True) #necessario para navegador não abrir e fechar automaticamente
chrome_options.add_argument('window-size=400,800') #Define o tamanho que vc quer do navegador
#chrome_options.add_argument('--headless')

servico = Service(ChromeDriverManager().install())#para realizar uma atualização do chrome driver para acompanhar a versao do Chrome
navegador = webdriver.Chrome(service=servico, options=chrome_options)

navegador.implicitly_wait(10)

navegador.get('https://www.catho.com.br/vagas/')

btn_close_add = navegador.find_element(By.ID, 'closeTimedAd')

print(btn_close_add.text)