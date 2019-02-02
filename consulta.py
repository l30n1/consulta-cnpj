import requests
import json
import time

# cnpj = ['05953543000309', '29954518000146']

'''
API de consulta
'''
base = 'https://www.receitaws.com.br/v1/cnpj/'


cnpj = []

with open('config.txt', 'r') as f:
    for line in f:
        codigo = line.replace('.', '').replace('/', '').replace('-', '').replace('\n', '').replace(' ', '')
        if codigo != '':
            cnpj.append(codigo)

    print("Arquivo carregado ...")

'''
Dict de controle
'''
check = {}
check['total'] = len(cnpj)
check['controle'] = len(cnpj)
check['tentativas'] = 0

'''
Gravação de Persistência
tenta acessar > caso erro outras tentativas são feitas
'''
with open('resultado.txt', 'w') as f:
    for i in cnpj:
        while not(check['tentativas'] > 4):
            r = requests.get(f'{base}{i}', timeout=5)
            print(f"[{check['controle']:02}/{check['total']}] - {check['tentativas']:02} - {r.status_code}")
            if r.status_code == requests.codes.ok:
                data = json.loads(r.text)
                check['tentativas'] = 2

                if data['status'] == 'OK':
                    print(f"{r.status_code} - {data['nome']}")
                    f.write(f"[{check['controle']:02}/{check['total']}] | cnpj: {data['cnpj']} | situacao: {data['situacao']} | nome: {data['nome']}\n")
                else:
                    print("erro!")
                    f.write(f"[{check['controle']:02}/{check['total']}] | cnpj: {i} | situacao: ERRO! | {data['message']}\n")

                check['controle'] -= 1
                if check['controle'] != 0:
                    time.sleep(20.5)
                break

            check['tentativas'] += 1
            time.sleep(1)

        if check['tentativas'] == 5:
            print('Erro: Impossivel conectar!')
            f.close()
            raise
        check['tentativas'] = 0
