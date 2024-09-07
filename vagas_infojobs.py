from bs4 import BeautifulSoup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from time import sleep


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

#Selecionar cidade
navegador.find_element(By.ID,'city').clear()
sleep(2)
input_place = navegador.find_element(By.ID,'city')
input_place.send_keys("Rio de Janeiro")
sleep(2)
hoverable = navegador.find_element(By.CLASS_NAME, "autocomplete-suggestion")
ActionChains(navegador).move_to_element(hoverable).perform()

clickable = navegador.find_element(By.CSS_SELECTOR, 'div[class*="autocomplete-selected"]')
ActionChains(navegador).click(clickable).perform()

#Clica botão achar vaga
s1 = "body > main > div.home-index-bg > section > div.job-location-filter > div.job-location-filter-btn > a"
btn_achar_vaga = navegador.find_element(By.CSS_SELECTOR, s1)
btn_achar_vaga.click()

#Pega lista de vagas
vagas_lista = navegador.find_elements(By.CSS_SELECTOR, "a[class='text-decoration-none']")
print(len(vagas_lista))
print(vagas_lista[1].get_attribute("outerHTML"))



#Teste
#Beneficios/escolraidade/habilidades
beneficios_lista = navegador.find_elements(By.CLASS_NAME, 'custom-list')
b1 = [BeautifulSoup(x.get_attribute("outerHTML"), 'html.parser') for x in beneficios_lista]
#print(b1[0].prettify())


########## Uma relção das referencias dos elementos de procura
#Titulo da vaga
'''s2 = "#VacancyHeader > div.d-flex.justify-content-between.text-break.mb-16 > div > h2"
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

#area profissional
area_profi = navegador.find_element(By.XPATH, '//*[@id="vacancylistDetail"]/div[2]/p[4]')
print(area_profi.text)

#Exiiegncia
exigencia = navegador.find_element(By.XPATH, '//*[@id="vacancylistDetail"]/div[2]/div[2]/ul/li')
print(exigencia.text)

#Exiiegncia
exigencias_lista = navegador.find_elements(By.XPATH, '//*[@id="vacancylistDetail"]/div[2]/div[4]/ul/li')
print(exigencias_lista[2].text)

#Exiiegncia
habilidades_lista = navegador.find_elements(By.CSS_SELECTOR, 'div[class*="tag-outline-primary"]')
print(habilidades_lista[2].text)'''







