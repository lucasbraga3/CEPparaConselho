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
first_string = f"SELECT ccs.nome, cisp.id, cisp.aisp as aisp,cisp.risp as risp,cisp.un_ter as un_ter, ccs.status FROM ((cisp_relacao INNER JOIN cisp ON cisp.id = cisp_relacao.idcisp)  INNER JOIN ccs ON ccs.id = cisp_relacao.idccs) where ccs.nome like '%{cidade}%' "
secondstr = f" or cisp.un_ter like '%{un_ter}%' limit 1"
if (un_ter == 'centro' or un_ter == 'Centro') and cidade != 'Rio de Janeiro':
    un_ter = cidade
cursor.execute(first_string + secondstr)
dado = cursor.fetchall()
if dado:
        print(f'Conselho: {dado[0][0]}')
        #print(f'CISP: {dado[0][1]}') #Removido pois nao é 100% preciso no momento
        print(f'AISP: {dado[0][2]}')
        print(f'RISP: {dado[0][3]}')
        print(f'UNIDADE TERRITORIAL: {dado[0][4]}') #Removido pois nao é 100% preciso no momento
        if dado[0][5] == 1:
            print('STATUS: Ativo')
        else: print('STATUS: Inativo')
else:
    print('Conselho não encontrado')