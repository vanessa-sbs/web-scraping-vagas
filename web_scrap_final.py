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
        return BeautifulSoup(response.text, 'html.parser')
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
    
def chrome_opcoes():#'https://www.infojobs.com.br/'
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) #necessario para navegador não abrir e fechar automaticamente
    #chrome_options.add_argument('window-size=1500,2000') #Define o tamanho que vc quer do navegador
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')

    servico = Service(ChromeDriverManager().install())#para realizar uma atualização do chrome driver para acompanhar a versao do Chrome
    return webdriver.Chrome(service=servico, options=chrome_options)


estados = ['sao paulo', 'rio de janeiro', 'minas gerais', 'bahia', 'distrito federal', 'santa catarina', 'Paraná', 'rio grande do sul']

vagas =[]

for estado in estados:

    navegador = chrome_opcoes()
    navegador.implicitly_wait(15)
    try:
        navegador.get('https://www.infojobs.com.br/')
    except:
        continue
    
    aceitar_cookies("didomi-notice-agree-button")

    clicar_estado(estado)

    num_vagas = len(navegador.find_elements(By.CSS_SELECTOR, "a[class='text-decoration-none']"))
    #total_vagas = int(navegador.find_element(By.CSS_SELECTOR, "span[class='small text-medium']").text.replace('.', ''))

    scroll(navegador, 1)

    print('QTS VAGAS: ', len(navegador.find_elements(By.CSS_SELECTOR, "a[class='text-decoration-none']")))
    print('Estado: ', estado)
    
    link_das_vagas = vagas_lista("a[class='text-decoration-none']")

    navegador.quit()

    for url in link_das_vagas:
        # Captura o valor do ID da vaga
        vaga_id = re.findall('[0-9]+', url)[0]  # Extrai o ID da vaga

        # Captura o valor do caminho relativo da URL
        vaga_href = url
      
        if requisicao_http(url):
            detalhes_soup = requisicao_http(url)
        else:
            continue 
         
        # Extrair o título da vaga
        titulo_element = detalhes_soup.find('h2', class_="js_vacancyHeaderTitle")
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



# Escreve os dados coletados em um arquivo JSON
#with open('vagas2.json', 'w', encoding='utf-8') as file:
#   json.dump(vagas, file, ensure_ascii=False, indent=4)

#################### TRATAEMNTOS DADOS ####################
import pandas as pd

df = pd.read_json(json.dump(vagas, ensure_ascii=False, indent=4))

#Separa cidade e sigla do estado da variavel local_da_empresa e cria duas colunas para cada 
df[['cidade_empresa', 'estado_empresa']] = df['local_da_empresa'].str.split('-', expand=True)
df_vagas = df.drop('local_da_empresa', axis=1)

#Cria colunas tipo_contrato e periodo_contrato a partir de tipo_de_contrato 
df_vagas[['tipo_contrato','periodo_contrato']] = df_vagas['tipo_de_contrato'].str.split(r'[-]+', expand=True)
df_vagas.drop('tipo_de_contrato', axis=1, inplace=True)

#Quebra faixa salaria em duas colunas: salario_min e salario_max
aux = df['faixa_salarial'].str.split(r'[\s]+', expand=True)
aux.drop([0,2,3,5,6], axis=1, inplace=True)
aux = aux.fillna(value='0')
df_vagas['salario_max'], df_vagas['salario_min']= aux[4].str.replace('.', '').str.replace(',', '.'), aux[1].str.replace('.', '').str.replace(',', '.').str.replace('a', '0')
df_vagas.drop('faixa_salarial', axis=1, inplace=True)

#Habilidades
df_vagas['habilidades'] = df_vagas['habilidades'].apply(lambda lista: [s.upper() for s in lista])

#Extrai de exigencias escolaridade minima e idiomas
df_exig = pd.DataFrame(df_vagas['exigencias'].to_list())

df_vagas['escolaridade_min'] =  df_exig[0].str.split(':').str[1]

df_vagas['idioma'] = df_exig[1].astype('str')

df_vagas['idioma'] = df_vagas['idioma'].apply(lambda x : x.split(','))
df_vagas['idioma'] = df_vagas['idioma'].apply(lambda lista: [{'language': s.split()[0], 'nivel': re.findall(r'\(([^]]+)\)', s)[0]} for s in lista] if lista != ['None'] else lista)

df_vagas.drop('exigencias', axis=1, inplace=True)

#Valorizado tiramos experiencia desejada
df_vagas['experiencia_desejada'] = df_vagas['valorizado'].apply(lambda s: s[0].split(':')[1] if ('Experiência desejada' in s[0])  else 'Não informado')
df_vagas.drop('valorizado', axis=1, inplace=True)

json_string = df.to_json(orient='records', indent=4)
#print("Dados salvos em vagas.json")





