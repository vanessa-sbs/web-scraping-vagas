from bs4 import BeautifulSoup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from time import sleep


chrome_options = Options()
chrome_options.add_experimental_option("detach", True) #necessario para navegador não abrir e fechar automaticamente
#chrome_options.add_argument('window-size=800,1000') #Define o tamanho que vc quer do navegador
chrome_options.add_argument('--headless')

servico = Service(ChromeDriverManager().install())#para realizar uma atualização do chrome driver para acompanhar a versao do Chrome
navegador = webdriver.Chrome(service=servico, options=chrome_options)

navegador.implicitly_wait(10)

navegador.get('https://www.infojobs.com.br/')

#Clica no botão aceitar
btn_close_cookies = navegador.find_element(By.ID, "didomi-notice-agree-button")
btn_close_cookies.click()

#Clica botão achar vaga
s1 = "body > main > div.home-index-bg > section > div.job-location-filter > div.job-location-filter-btn > a"
btn_achar_vaga = navegador.find_element(By.CSS_SELECTOR, s1)
btn_achar_vaga.click()

#Titulo da vaga
s2 = "#VacancyHeader > div.d-flex.justify-content-between.text-break.mb-16 > div > h2"
titulo_vaga = navegador.find_element(By.CSS_SELECTOR, s2)
print(titulo_vaga.text)

#Empresa
empresa = navegador.find_element(By.CSS_SELECTOR, "div[class='h4']")
print(empresa.text)

#Salario
salario = navegador.find_element(By.XPATH, '//*[@id="VacancyHeader"]/div[1]/div/div[2]/div[2]')
print(salario.text)

#modelo trabalho
modelo_trabalho = navegador.find_element(By.XPATH, '//*[@id="VacancyHeader"]/div[1]/div/div[2]/div[3]')
print(modelo_trabalho.text)

#sobre a vaga
desc_vaga = navegador.find_element(By.XPATH, '//*[@id="vacancylistDetail"]/div[2]/p[1]')
print(desc_vaga.text)

#numero de vagas
num_vagas = navegador.find_element(By.XPATH, '//*[@id="vacancylistDetail"]/div[2]/p[2]')
print(num_vagas.text)

#tipo contrato
tipo_contrato = navegador.find_element(By.XPATH, '//*[@id="vacancylistDetail"]/div[2]/p[3]')
print(tipo_contrato.text)

