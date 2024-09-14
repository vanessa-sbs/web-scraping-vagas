from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver import ActionChains

from time import sleep, time
import re

inicio = time()
print('Rodando....')

#Clica no botão aceitar cookies
def aceitar_cookies(element_id):
    btn_close_cookies = navegador.find_element(By.ID, element_id)
    btn_close_cookies.click()

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

def scroll(driver, qtd_scroll):
   
    i = 0
    while i <= qtd_scroll:
        #altura = navegador.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(5)
        i = i+1


def vagas_lista(referencia_css_selector):
    #navegador.execute_script("window.scrollTo("+str(h1)+",document.body.scrollHeight)")
    vagas_link = []
    links = navegador.find_elements(By.CSS_SELECTOR, referencia_css_selector)
    for link in links:
        vagas_link.append(link.get_attribute('href') )
    
    return(vagas_link)

def verifica_elemento(html_content, elemento):
    exigencias_section = html_content.find('div', class_='h4 font-weight-bold text-body mb-12', string=lambda t: elemento in t)
    if exigencias_section:
        ul_element = exigencias_section.find_next('ul')
        return [li.text.strip() for li in ul_element.find_all('li')] if ul_element else [elemento + ' não identificadas']
    else:
        return [elemento + ' não identificadas']
    
def requisicao_http(url):
    # Realiza a requisição HTTP para a URL de listagem de vagas
    try:
        response = requests.get(url)
        #response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except:
        print(f"Erro ao acessar detalhes da vaga: {url}")

def format_text(text):
    text = text.replace('\r\n', '').strip()  # Remove quebras de linha
    text = ' '.join(text.split())  # Remove espaços extras
    return text

def verifica_elemento(html_content, elemento):
    soup = html_content.find('div', class_='h4 font-weight-bold text-body mb-12', string=lambda t: elemento in t)
    if soup:
        ul_element = soup.find_next('ul')
        return [li.text.strip() for li in ul_element.find_all('li')] if ul_element else [elemento + ' não identificadas']
    else:
        return [elemento + ' não identificadas']
    

chrome_options = Options()
chrome_options.add_experimental_option("detach", True) #necessario para navegador não abrir e fechar automaticamente
#chrome_options.add_argument('window-size=1500,2000') #Define o tamanho que vc quer do navegador
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--incognito')

servico = Service(ChromeDriverManager().install())#para realizar uma atualização do chrome driver para acompanhar a versao do Chrome
navegador = webdriver.Chrome(service=servico, options=chrome_options)

navegador.implicitly_wait(15)
navegador.get('https://www.infojobs.com.br/')

lista_estados = ['sao paulo', 'rio de janeiro', 'minas gerais', 'bahia', 'distrito federal', 'santa catarina', 'Paraná', 'rio grande do sul']

for estado in lista_estados:
    
    aceitar_cookies("didomi-notice-agree-button")

    clicar_estado(estado)

    num_vagas = len(navegador.find_elements(By.CSS_SELECTOR, "a[class='text-decoration-none']"))
    #total_vagas = int(navegador.find_element(By.CSS_SELECTOR, "span[class='small text-medium']").text.replace('.', ''))

    scroll(navegador, 0)

    print('QTS VAGAS: ', len(navegador.find_elements(By.CSS_SELECTOR, "a[class='text-decoration-none']")))

    link_das_vagas = vagas_lista("a[class='text-decoration-none']")

    navegador.quit()

    vagas =[]
    j = 0
    for url in link_das_vagas:
        # Captura o valor do ID da vaga
        vaga_id = re.findall('[0-9]+', url)[0]  # Extrai o ID da vaga

        # Captura o valor do caminho relativo da URL
        vaga_href = url

        # Monta a URL completa para os detalhes da vaga
        #detalhes_url = f"https://www.infojobs.com.br{vaga_href}"
        print("vaga: ", j)
        try:
            detalhes_soup = requisicao_http(url)
        except:
            continue
        
        # Extrair o título da vaga
        titulo_element = detalhes_soup.find('h2')
        titulo = titulo_element.text.strip() if titulo_element else 'Título não disponível'

        # Extrair o Nome da empresa da vaga
        empresa_element = detalhes_soup.find('div', class_='h4').find('a')
        empresa = empresa_element.text.strip() if empresa_element else 'Empresa confidencial'

        descricao_element = detalhes_soup.findAll('p')#, attrs={'class': 'mb-16 text-break white-space-pre-line'})
        descricao = format_text(descricao_element[0].text.strip())

        # Extrair o local e a faixa salarial
        divs = detalhes_soup.find_all('div', class_='text-medium mb-4')
        local = divs[0].contents[0].strip() if len(divs) > 0 else 'Local não identificado'
        faixa_salarial = divs[1].contents[0].strip() if len(divs) > 1 else 'Faixa salarial não informada'
        faixa_salarial = format_text(faixa_salarial)  # Formatar a faixa salarial

        # Extrair o Modelo de trabalho
        modelo_element = detalhes_soup.find('div', class_='text-medium small font-weight-bold mb-4')
        modelo = modelo_element.text.strip() if modelo_element else 'Modelo de trabalho não identificado'

        # Extrair o tipo de contrato de trabalho
        contrato_element = detalhes_soup.find('span', string='Tipo de contrato e Jornada:')
        contrato = contrato_element.find_next_sibling(string=True).strip() if contrato_element else 'Tipo de contrato de trabalho não identificado'

        # Extrair Exigências
        exigencias = verifica_elemento(detalhes_soup, 'Exigências')

        # Extrair Valorizado
        valorizado = verifica_elemento(detalhes_soup, 'Valorizado')

        # Extrair Benefícios
        beneficios = verifica_elemento(detalhes_soup, 'Beneficios')

        # Extrair Habilidades
        habilidades_element = detalhes_soup.find_all('div', class_='tag mr-8 mb-8 tag-outline-primary tag-lg')
        habilidades = [habilidade.find('span').text.strip() for habilidade in habilidades_element] if habilidades_element else ['Habilidades não identificadas']


        # Adiciona os dados coletados na lista de vagas
        vagas.append({
            'id_da_vaga': vaga_id,
            'titulo_da_vaga': titulo,
            'nome_da_empresa': empresa,
            'local_da_empresa': local,
            'modelo_de_trabalho': modelo,
            'tipo_de_contrato': contrato,
            'faixa_salarial': faixa_salarial,
            'descricao_da_vaga': descricao,
            'exigencias': exigencias,
            'valorizado': valorizado,
            'beneficios': beneficios,
            'habilidades': habilidades,
            'url_da_vaga': vaga_href
        })

        j = j+1


# Escreve os dados coletados em um arquivo JSON
with open('vagas.json', 'w', encoding='utf-8') as file:
   json.dump(vagas, file, ensure_ascii=False, indent=4)

print("Dados salvos em vagas.json")

fim = time()

print(fim - inicio)




