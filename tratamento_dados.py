import pandas as pd
import re

df = pd.read_json('vagas2.json')

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