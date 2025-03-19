import psycopg2
import os
import brazilcep
from unidecode import unidecode
from dotenv import load_dotenv
# Connectando ao banco de dados
load_dotenv('truedbdata.env')
dbname = os.getenv('DB_NAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
port = os.getenv('PORT')
host = os.getenv('HOST')
conn = psycopg2.connect(dbname=dbname, user=user, password=password, port=port, host=host)
 
# Recebendo o CEP
while(1==1):
    cep = input('Digite o CEP: ')
    try: 
        endereco = brazilcep.get_address_from_cep(cep)
    except:
        raise Exception('CEP inválido')
        
    un_ter = unidecode(endereco['district']).upper()
    cidade = unidecode(endereco['city']).upper()
    cursor = conn.cursor()
    first_string = f"SELECT ccs.nome, cisp.id, cisp.aisp as aisp,cisp.risp as risp,cisp.un_ter as un_ter, ccs.status FROM ((cisp_relacao INNER JOIN cisp ON cisp.id = cisp_relacao.idcisp)  INNER JOIN ccs ON ccs.id = cisp_relacao.idccs) INNER JOIN unidade_territorial on cisp.id = unidade_territorial.idcisp where unidade_territorial.municipio = '{cidade}' "
    secondstr = f" AND unidade_territorial.nome = '{un_ter}'"
    finalstr = f"order by UPPER(ccs.nome) <-> '{cidade}'"
    cursor.execute(first_string + secondstr )
    dado = cursor.fetchall()
    if dado:
            print('precisão: 100%')
            print(f'Conselho: {dado[0][0]}')
            print(f'CISP: {dado[0][1]}') #pode ser removido pois nao é 100% preciso no momento
            print(f'AISP: {dado[0][2]}')
            print(f'RISP: {dado[0][3]}')
            #print(f'UNIDADE TERRITORIAL: {dado[0][4]}') #Removido pois nao é 100% preciso no momento
            if dado[0][5] == 1:
                print('STATUS: Ativo')
            else: print('STATUS: Inativo')
    else:
        #un_ter = cidade
        cursor.execute(first_string + finalstr)
        dado = cursor.fetchall()
        if dado:
                print('Precisão: 70%')
                print(f'Conselho: {dado[0][0]}')
                print(f'CISP: {dado[0][1]}') # pode ser removido pois nao é 100% preciso no momento
                print(f'AISP: {dado[0][2]}')
                print(f'RISP: {dado[0][3]}')
                if dado[0][5] == 1:
                    print('STATUS: Ativo')
                else: print('STATUS: Inativo')
        else:
             print('não encontrado')
