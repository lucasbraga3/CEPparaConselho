import psycopg2
import os
import brazilcep
from unidecode import unidecode
from dotenv import load_dotenv
# Connectando ao banco de dados
load_dotenv('dbdata.env')
dbname = os.getenv('DB_NAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
port = os.getenv('PORT')
host = os.getenv('HOST')
conn = psycopg2.connect(dbname=dbname, user=user, password=password, port=port, host=host)
 
# Recebendo o CEP

cep = input('Digite o CEP: ')
endereco = brazilcep.get_address_from_cep(cep)
un_ter = unidecode(endereco['district'])
cidade = unidecode(endereco['city'])

# Consultando os dados CEP no banco de dados

cursor = conn.cursor()
first_string = f"SELECT ccs.nome, cisp.id, cisp.aisp as aisp,cisp.risp as risp,cisp.un_ter as un_ter FROM ((cisp_relacao INNER JOIN cisp ON cisp.id = cisp_relacao.idcisp)  INNER JOIN ccs ON ccs.id = cisp_relacao.idccs) where ccs.nome like '%{cidade}%' or cisp.un_ter like '%{un_ter}%' limit 1"
cursor.execute(first_string)
dados = cursor.fetchall()
if dados:
    for dado in dados:
        print(f'Conselho: {dado[0]}')
        print(f'CISP: {dado[1]}')
        print(f'AISP: {dado[2]}')
        print(f'RISP: {dado[3]}')
        print(f'UNIDADE TERRITORIAL: {dado[4]}')
else:
    print('CEP não encontrado')