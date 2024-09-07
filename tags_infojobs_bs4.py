import requests
from bs4 import BeautifulSoup
import json

# URL da página de busca de vagas
url = "https://www.infojobs.com.br/vaga-de-trabalhe-casa-lider-analista-pessoal-em-rio-janeiro__9904879.aspx"

# Realiza a requisição HTTP para a URL
response = requests.get(url)
response.raise_for_status()  # Checa se a requisição foi bem-sucedida

# Analisa o conteúdo HTML com BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser').find('form')

# Extração das informações desejadas com as classes corretas
titulo_element = soup.find('h2')
titulo = titulo_element.text.strip() if titulo_element else 'Título não disponível'
print(titulo)

empresa_element = soup.find('a', attrs={'target': '_blank'})
empresa = empresa_element.text.strip() if empresa_element else 'Empresa confidencial'
print(empresa)

elementos1 = soup.findAll('div', class_='text-medium mb-4')
local = elementos1[0].text.strip()
salario = elementos1[1].text.strip()
print(salario)
print(local)

descricao_element = soup.find('p', attrs={'class': 'mb-16 text-break white-space-pre-line'})
descricao = descricao_element.text.strip()
#print(descricao)

modelo_trabalho_element = soup.findAll('p')
modelo_trabalho = modelo_trabalho_element[2].text
print(modelo_trabalho)

#Exigencias/ Valorizado/Beneficios
elementos2 = soup.findAll('li')
for x in elementos2:
    print(x.text)

#Habilidades
elementos3 = soup.findAll('div', class_ = 'tag mr-8 mb-8 tag-outline-primary tag-lg')
print('Habilidades:')
for x in elementos3:
    print(x.find('span').text)