from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver import ActionChains

from time import sleep

def clicar_estado(estado):
    navegador.find_element(By.ID,'city').clear()
    sleep(2)
    input_place = navegador.find_element(By.ID,'city')
    input_place.send_keys(estado)
    sleep(2)
    
    hoverable = navegador.find_elements(By.CLASS_NAME, "autocomplete-suggestion")[-1]
    ActionChains(navegador).move_to_element(hoverable).perform()

    clickable = navegador.find_element(By.CSS_SELECTOR, 'div[class*="autocomplete-selected"]')
    ActionChains(navegador).click(clickable).perform()

    #Clica botão achar vaga
    s1 = "body > main > div.home-index-bg > section > div.job-location-filter > div.job-location-filter-btn > a"
    btn_achar_vaga = navegador.find_element(By.CSS_SELECTOR, s1)
    btn_achar_vaga.click()

def scroll():
    #Tentativa de simular scroll para pegar as proximas vagas
    #altura = navegador.execute_script("return document.body.scrollHeight")
    #print(altura)
    h1 = navegador.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    print(type(h1))
    sleep(5)

def vagas_lista(referencia_css_selector): #"a[class='text-decoration-none']"
    #navegador.execute_script("window.scrollTo("+str(h1)+",document.body.scrollHeight)")
    #Pega primeira lista de vagas
    vagas_link = []
    links = navegador.find_elements(By.CSS_SELECTOR, referencia_css_selector)
    for link in links:
        vagas_link.append(link.get_attribute('href') )
    
    return(vagas_link)


chrome_options = Options()
chrome_options.add_experimental_option("detach", True) #necessario para navegador não abrir e fechar automaticamente
#chrome_options.add_argument('window-size=1500,2000') #Define o tamanho que vc quer do navegador
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--incognito')

servico = Service(ChromeDriverManager().install())#para realizar uma atualização do chrome driver para acompanhar a versao do Chrome
navegador = webdriver.Chrome(service=servico, options=chrome_options)

navegador.implicitly_wait(15)

navegador.get('https://www.infojobs.com.br/')

#Clica no botão aceitar
btn_close_cookies = navegador.find_element(By.ID, "didomi-notice-agree-button")
btn_close_cookies.click()

#Selecionar estado
#navegador.find_element(By.ID,'city').clear()
#sleep(2)
#input_place = navegador.find_element(By.ID,'city')
#lista_estados = ['sao paulo', 'rio de janeiro', 'minas gerais', 'bahia', 'distrito federal', 'santa catarina', 'Paraná', 'rio grande do sul']

clicar_estado("minas gerais")

scroll()

link_das_vagas = vagas_lista("a[class='text-decoration-none']")

print(link_das_vagas)



