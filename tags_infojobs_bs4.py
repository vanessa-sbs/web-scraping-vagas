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

aux1_elements = soup.findAll('div', class_='text-medium mb-4')
local = aux1_elements[0].text.strip()
salario = aux1_elements[1].text.strip()
print(salario)
print(local)

descricao_element = soup.findAll('p')#, attrs={'class': 'mb-16 text-break white-space-pre-line'})
descricao = descricao_element[0].text.strip()
contrato = descricao_element[2].text.strip()
print(contrato)

modelo_trabalho_element = soup.find('div', class_= "text-medium small font-weight-bold mb-4")
modelo_trabalho = modelo_trabalho_element.text.strip()
print(modelo_trabalho)

#Exigencias/ Valorizado/ Beneficios
aux = soup.findAll('div', class_ = "h4 font-weight-bold text-body mb-12")
aux2 = soup.findAll('li')
for i in (0, len(aux)-1):
    if aux[i]:
        print(aux[i].text.strip() + aux2[i].text.strip())
    else:
        print('nao encontrado')

#Habilidades
elementos3 = soup.findAll('div', class_ = 'tag mr-8 mb-8 tag-outline-primary tag-lg')
print('Habilidades:')
for x in elementos3:
    print(x.find('span').text)